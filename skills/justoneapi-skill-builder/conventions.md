# JustOneAPI Skill 代码规范

本文是新 skill 编写时的**强制规范**。逐节对齐，不要"优化"。

## 脚本头（PEP 723）

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# <script_name>.py —— <一句话功能>，每页先 upsert 到 GoodGame 后端，再落 CSV
# 用法：uv run <script_name>.py <required_arg> [optional_arg ...] [--output-dir DIR] [其它选项]
# 示例：uv run <script_name>.py <demo_value> --output-dir ./output
```

唯一第三方依赖只允许 `requests`，由 `uv run` 自动装。

## Token 加载（逐字复制，不要改）

```python
def load_token():
    for d in [Path.cwd(), *Path.cwd().parents]:
        p = d / ".env"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                for k in ("JUSTONEAPI_TOKEN", "JUST_ONE_API_TOKEN"):
                    if line.startswith(f"{k}=") and (v := line.split("=", 1)[1].strip()):
                        return v
    v = os.environ.get("JUSTONEAPI_TOKEN") or os.environ.get("JUST_ONE_API_TOKEN")
    if v:
        return v
    sys.exit("❌ 未找到 JustOneAPI Token，请在 .env 中配置：\n  JUSTONEAPI_TOKEN=your_token")
```

## 错误码表（SKILL.md 必须含此表）

> ⚠️ `code` 在**响应体**中，不是 HTTP 状态码。HTTP 200 也须检查 `code`。

| `code` | 含义 | 处理策略 |
|:------:|------|----------|
| `0` | 成功 | 正常处理 |
| `100` | Token 无效或已失效 | 提示用户检查 token |
| `301` | 采集失败 | **自动重试**，间隔 2-3 秒，最多 3 次 |
| `302` | 超出速率限制 | 降低请求频率，等待后重试 |
| `303` | 超出每日配额 | 告知用户当日配额已用尽 |
| `400` | 参数错误 | 检查必填参数是否缺失或格式有误 |
| `500` | 服务器内部错误 | 稍后重试，持续则反馈 JustOneAPI |
| `600` | 权限不足 | 告知用户当前 token 无此接口权限 |
| `601` | 余额不足 | 告知用户需在 JustOneAPI 充值 |

## 公共常量

```python
TIMEOUT        = 60
RETRY_MAX      = 3
RETRY_SLEEP    = 2.0
PAGE_SLEEP     = 0.1
NO_RETRY_CODES = {100, 303, 400, 600, 601}   # 评论脚本用：这些 code 不重试，直接结束本任务
_CST = timezone(timedelta(hours=8))
```

## 公共工具函数

```python
def fmt_cst(ts) -> str:
    try:
        return datetime.fromtimestamp(int(ts), tz=_CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""

def _safe_int(v):
    try: return int(v)
    except (TypeError, ValueError): return None

def _code_eq(code, target: int) -> bool:
    """JustOneAPI 各接口 code 有时是 int 有时是 str，统一比较。"""
    try: return int(code) == target
    except (TypeError, ValueError): return str(code) == str(target)

def _pick(d, *keys, default=None):
    """从 dict 中按候选键名顺序取第一个非空值。字段兜底必备。"""
    for k in keys:
        if d is None: break
        v = d.get(k)
        if v not in (None, "", [], {}): return v
    return default
```

## 字段名兜底

JustOneAPI 文档里 `data` 经常只标 `object`，**真实字段名要靠跑一次接口看响应**。脚本中所有字段提取都通过 `_pick(...)` 多名兜底，常见兜底候选：

| 用途 | 候选键 |
|------|--------|
| 列表节点 | `posts` / `items` / `notes` / `data` |
| 翻页游标 | `next_pagination_token` / `pagination_token` / `next_max_id` / `next_min_id` / `cursor` / `lastCursor` |
| 数字 ID | `pk` / `id` / `media_id`（注意去掉 `_user` 后缀：`"3123_1234567" → "3123"`） |
| 时间戳 | `taken_at` / `created_at` / `created_at_utc` / `create_time` / `device_timestamp` / `time` |
| 文本 | `text` / `content` / `desc` / `caption.text`（`caption` 可能是 dict 也可能是 str，要判类型） |
| 点赞 | `like_count` / `comment_like_count` / `likes` / `liked_count` |
| 评论数 | `comment_count` / `comments_count` / `child_comment_count` / `reply_count` / `sub_comment_count` |
| has_more | `more_available` / `has_more` / `has_more_comments`（None 时 fallback 到 `bool(next_cursor)`） |

**响应可能多嵌一层 `data`**（实测 IG `get-user-posts` 返回的是 `body.data.data.items`），`fetch_page` 必须做解包：

```python
if _code_eq(body.get("code"), 0):
    d = body.get("data") or {}
    inner = d.get("data") if isinstance(d.get("data"), dict) else None
    if inner and any(k in inner for k in ("items", "posts", "comments", "users")):
        # 把外层游标提到内层，方便统一处理
        for ck in ("pagination_token", "next_pagination_token",
                   "next_max_id", "next_min_id", "more_available"):
            if ck in d and ck not in inner:
                inner[ck] = d[ck]
        return inner
    return d
```

## 重试逻辑

`fetch_page` 统一形态（HTTP 异常 + `code=301` 都触发重试）：

```python
for attempt in range(1, RETRY_MAX + 1):
    try:
        r = requests.get(API_URL, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        if _code_eq(body.get("code"), 0):
            return body.get("data") or {}
        code = body.get("code")
        if _code_eq(code, 301) and attempt < RETRY_MAX:
            time.sleep(RETRY_SLEEP); continue
        print(f"  [warn] code={code} (attempt {attempt})")
    except Exception as e:
        print(f"  [error] {e} (attempt {attempt})")
    if attempt < RETRY_MAX:
        time.sleep(RETRY_SLEEP)
return None
```

## 脚本结构

两种范式，按接口语义二选一。**不要发明第三种**。

### 范式 A：列表型（多线程，单层翻页）

适用：搜索接口、用户主页帖子列表、用户列表。代表：`scripts/get_user_posts.py`、`scripts/search_*.py`。

骨架：

1. 模块级常量：`API_URL` / `CSV_COLUMNS` / `BACKEND_URL` / `UPLOAD_FIELD_MAP` / `INT_FIELDS`
2. `Ctx` dataclass：`token / since_ts / max_pages / writer / fp / csv_lock / seen_ids / progress / pfile / prog_lock / trace_id / failed_path / failed_lock`
3. `fetch_<entity>(ctx, entity_id)`：单实体翻页循环
4. `main()`：argparse → 打开 CSV → `ThreadPoolExecutor(max_workers=args.workers)` 派发

锁内 / 锁外职责（顺序固定）：

```python
# 1) 锁内：CSV 去重 + 标记已见
with ctx.csv_lock:
    new = [r for r in rows if r["pk"] and r["pk"] not in ctx.seen_ids]
    for r in new: ctx.seen_ids.add(r["pk"])

# 2) 锁外：先 upload，再写 CSV
if new:
    upload_to_backend(new, ctx)
    with ctx.csv_lock:
        for r in new:
            csv_row = {**r, "raw_json": json.dumps(r["raw_json"], ensure_ascii=False)}
            ctx.writer.writerow(csv_row)
        ctx.fp.flush()
```

必备 CLI 选项：`positional_ids+`、`--output-dir`、`--workers`（默认 3）、`--max-pages`、`--since YYYY-MM-DD`（如适用）。

### 范式 B：评论两阶段（单线程，顶层 → 子回复）

适用：评论接口（顶层 + 楼中楼）。代表：`scripts/get_note_comments.py`、`scripts/get_post_comments.py`。

骨架：

1. 两个 endpoint：`TOP_ENDPOINT` / `SUB_ENDPOINT`
2. 阶段 1 抓顶层评论，记录每条的 `child_comment_count > 0` 的列表
3. 阶段 2 对 1 中每条父评论调 SUB endpoint 抓全部回复，写入同一个 CSV（`is_sub=1, parent_comment_id=...`）
4. 进度文件按"任务"维度组织：`{task_key: {phase: "top"|"sub", cursor, current_parent_id, ...}}`，task_key 用 `code` 或 `code:media_id`
5. **强制单线程**（评论数据量大、子评论翻页串行更稳，不要加并发）

必备 CLI 选项：`positional_codes+`、`--output-dir`、`--sort`、`--max-top N`（顶层评论上限）、`--no-replies`（跳过阶段 2）。

## 后端文件分层规范

GoodGame 后端在 `/Users/noir/Projects/GoodGame/`，新平台 upsert 接口由 agent 自助实现，**严格按下面 6 个文件分层**。已有 `skill_data_xiaohongshu` / `skill_data_instagram` 作为参考实现，新平台直接 copy 同名文件改字段即可。

### 1. ORM Model：`backend/KOL/orm/skill/<platform>_models.py`

Pydantic Model，字段一一对应 Supabase 表。命名 `<Platform><Entity>`（如 `XiaohongshuNote`、`InstagramPost`）。

```python
class <Platform><Entity>(BaseModel):
    """<中文说明>。 唯一约束: <biz_pk>"""
    id: Optional[int] = Field(default=None, ge=1)
    <biz_pk>: str
    # ... 业务字段（与 DDL 一一对应，全部 Optional）
    raw_data: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### 2. ORM Repository：`backend/KOL/orm/skill/<platform>_repositories.py`

每个 Model 一个 Repository 类。**必备方法**：`upsert` / `bulk_upsert` / `get_by_<biz_pk>` / `_row_to_model`，可选 `list_by_xxx`。

```python
class <Platform><Entity>Repository:
    TABLE = "gg_skill_<platform>_<entity>"
    # 复合主键时再加 ON_CONFLICT
    ON_CONFLICT = "<biz_pk>,comment_id"

    @staticmethod
    def bulk_upsert(items: List[Union[<Model>, Dict[str, Any]]]) -> List[<Model>]:
        if not items: return []
        client = get_client()
        payloads = []
        for it in items:
            payload = it.model_dump(mode="json", exclude_none=True) if hasattr(it, "model_dump") else dict(it)
            if payload.get("id") is None: payload.pop("id", None)
            payloads.append(payload)
        resp = client.table(<Repo>.TABLE).upsert(payloads, on_conflict="<biz_pk>").execute()
        return [<Repo>._row_to_model(r) for r in (resp.data or [])]

    @staticmethod
    def _row_to_model(row): return <Model>(**row) if row else <Model>(<biz_pk>="")
```

复合键评论表的 `bulk_upsert` 把 `on_conflict` 改成 `<Repo>.ON_CONFLICT` 即可。

### 3. ORM 包导出：`backend/KOL/orm/skill/__init__.py`

```python
from .<platform>_models import <Model1>, <Model2>, ...
from .<platform>_repositories import <Repo1>, <Repo2>, ...

__all__ = [..., "<Model1>", "<Repo1>", ...]   # 追加，别覆盖现有项
```

### 4. API Schema：`backend/api/schemas/skill_data_<platform>.py`

每个资源四件套：`<X>UpsertItem` / `<X>UpsertRequest(BaseRequest)` / `<X>UpsertResult` / `<X>Ref`（仅复合键时）。

```python
class <Platform><Entity>UpsertItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    <biz_pk>: str = Field(..., min_length=1, description="...（唯一键）")
    # 其余字段全 Optional，不设默认值

class <Platform><Entity>UpsertRequest(BaseRequest):
    model_config = ConfigDict(extra="ignore", json_schema_extra={"example": {...}})
    items: List[<Platform><Entity>UpsertItem] = Field(default_factory=list)

class <Platform>UpsertResult(BaseModel):
    count: int = Field(0)
    ids: List[str] = Field(default_factory=list)   # 复合键时改 items: List[<Ref>]
```

### 5. API Router：`backend/api/routers/skill_data_<platform>.py`

```python
from fastapi import APIRouter
from jobs.logger import get_logger
from ..schemas.base import BaseResponse
from ..schemas.skill_data_<platform> import <X>UpsertRequest, <X>UpsertResult
from KOL.orm.skill import <X>Repository

logger = get_logger(__name__)
router = APIRouter()

@router.post("/skill/<platform>/<resource>/upsert", response_model=BaseResponse[<X>UpsertResult])
async def upsert_<platform>_<resource>(body: <X>UpsertRequest) -> BaseResponse[<X>UpsertResult]:
    """批量 upsert ..."""
    if not body.items:
        return BaseResponse.ok(<X>UpsertResult(count=0, ids=[]), trace_id=body.trace_id)
    payloads = [it.model_dump(mode="json", exclude_unset=True) for it in body.items]
    logger.info("【<resource> upsert】trace_id=%s 待写入条数=%d", body.trace_id, len(payloads))
    saved = <X>Repository.bulk_upsert(payloads)
    ids = [x.<biz_pk> for x in saved if getattr(x, "<biz_pk>", None)]
    return BaseResponse.ok(<X>UpsertResult(count=len(saved), ids=ids), trace_id=body.trace_id)
```

`exclude_unset=True` 关键 —— 避免把客户端没传的字段覆盖成 NULL。

### 6. Server 注册：`backend/api/server.py`

两处改动（追加，不要重写整个文件）：

```python
# import 行追加新 router
from .routers import (..., skill_data_xiaohongshu, skill_data_instagram, skill_data_<platform>)

# create_app() 内追加挂载
app.include_router(skill_data_<platform>.router, prefix="/api", tags=["skill-<platform>"])
```

### 自查

- [ ] 6 个文件全部落盘 / 修改完成
- [ ] Repository `TABLE` 名与 DDL 表名一致
- [ ] Schema `UpsertItem` 字段与 ORM Model 字段一致（Optional 默认 None，不设默认值）
- [ ] Router URL 与脚本里的 `BACKEND_URL` 完全对齐（含 `/api` 前缀）
- [ ] `server.py` 的 import 与 `include_router` 都已追加
- [ ] 不需要写后端单测

## 后端 upsert

> **强制规范**：每个采集脚本都必须接入后端 upsert，不存在"只落 CSV 不上传"的脚本。无需向用户确认是否需要 upsert，直接实现。

URL 约定：`POST https://www.goodgame.monster/api/skill/<platform>/<resource>/upsert`

请求体：

```json
{ "trace_id": "<prefix>_<YYYYMMDD_HHMMSS>", "items": [ {...}, {...} ] }
```

响应：`{"code": 0, "data": {"count": 12}}`。

实现要点：

- `to_upload_item(row)` 做 CSV 列名 → schema 字段名映射 + 类型转换 + 空值剔除
- `INT_FIELDS` 集合标记必须转 int 的字段，转失败则 drop 整字段
- 失败处理：`HTTP != 200` 或 `body.code != 0` → 把整页 `items` append 到 `<prefix>_failed.jsonl`，**不抛异常**，继续翻下一页
- `trace_id` 全程一致：`f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"`，main() 入口生成一次

```python
def upload_to_backend(rows: list, ctx: Ctx) -> bool:
    items = [to_upload_item(r) for r in rows]
    items = [it for it in items if it.get("<biz_pk>")]
    if not items: return True
    try:
        resp = requests.post(BACKEND_URL,
            json={"trace_id": ctx.trace_id, "items": items}, timeout=UPLOAD_TIMEOUT)
        body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        if resp.status_code == 200 and body.get("code") == 0:
            print(f"  ↑ 上传到后端 {body.get('data', {}).get('count', 0)} 条"); return True
        print(f"  ⚠️ 上传到后端失败 HTTP={resp.status_code} body={body}")
    except Exception as e:
        print(f"  ⚠️ 上传到后端异常: {e}")
    with ctx.failed_lock, open(ctx.failed_path, "a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False, default=str) + "\n")
    return False
```

## 断点续传

三类状态文件，固定命名：

| 文件 | 内容 | 何时清空 |
|------|------|----------|
| `<csv_name>.csv` | 主数据，**追加写**，第一行 header | 不主动清，靠 `seen_ids` 去重 |
| `.<prefix>_<type>_progress.json` | `{entity_id: {cursor, page, total, ...}}` | 该 entity 完成时 `progress.pop(entity_id)` |
| `<prefix>_<type>_failed.jsonl` | 后端 upsert 失败的整页 payload，每行一个 item | 不主动清，事后人工补传 |

启动时：

```python
seen_ids   = load_seen(csv_file)               # 从 CSV 读所有业务主键
progress   = load_progress(pfile)              # 读上次的游标
file_exists = csv_file.exists() and csv_file.stat().st_size > 0
```

写 CSV 时 `with open(csv_file, "a", newline="", encoding="utf-8-sig")`，未创建过才写 header。

`save_progress` 每页都调一次（同步落盘），`progress.pop(entity_id)` 表示该实体已完成。

## Supabase DDL 模板

后端是 Supabase（PostgreSQL）。表前缀统一 `gg_skill_<platform>_`，必备列：自增 PK、业务唯一键、`raw_data JSONB`、`created_at / updated_at TIMESTAMPTZ`。

### 主表（列表型实体）

```sql
CREATE TABLE IF NOT EXISTS public.gg_skill_<platform>_<entity> (
  id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  <owner_field>   TEXT        NOT NULL,                  -- 抓取入参（爬取归属，如 username / userId / keyword）
  <biz_pk>        TEXT        NOT NULL,                  -- 平台原生业务主键
  -- ... 业务列（int/text/timestamp）...
  raw_data        JSONB,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uk_<platform>_<entity>_pk UNIQUE (<biz_pk>)
);

CREATE INDEX IF NOT EXISTS idx_<platform>_<entity>_owner_time
  ON public.gg_skill_<platform>_<entity> (<owner_field>, <time_col> DESC);
```

### 评论表（含子回复）

复合唯一键 `(主键, comment_id)`，`is_sub / parent_comment_id / root_comment_id` 三件套：

```sql
CREATE TABLE IF NOT EXISTS public.gg_skill_<platform>_<parent>_comments (
  id                 BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  <biz_pk>           TEXT     NOT NULL,
  comment_id         TEXT     NOT NULL,
  parent_comment_id  TEXT,
  root_comment_id    TEXT,
  is_sub             SMALLINT NOT NULL DEFAULT 0,
  -- ... content / like_count / reply_count / user_* / comment_time ...
  raw_data           JSONB,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uk_<platform>_comments UNIQUE (<biz_pk>, comment_id)
);
```

### 共享 updated_at 触发器（项目内只需建一次）

```sql
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

DROP TRIGGER IF EXISTS trg_<table>_updated_at ON public.<table>;
CREATE TRIGGER trg_<table>_updated_at
  BEFORE UPDATE ON public.<table>
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
```

RLS 默认关闭（service role 写入），无需配 policy。

## 测试规范

每脚本一个 case，**真实调接口，不要 mock**。位置 `skills/<platform>-justoneapi/tests/test_scripts_smoke.py`。

骨架（参考 `skills/instagram-justoneapi/tests/test_scripts_smoke.py`）：

```python
import importlib.util, io, os, sys, tempfile, unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
TEST_<OWNER> = os.environ.get("<PLATFORM>_TEST_<OWNER>", "<default_public_account>")

def _load(name):
    spec = importlib.util.spec_from_file_location(f"_t_{name}", SCRIPTS_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class ScriptsSmokeTest(unittest.TestCase):
    test_pk: str = ""

    @classmethod
    def setUpClass(cls):
        """先调一次列表接口拿一个稳定 pk 给评论测试用，避免硬编码失效。"""
        m = _load("get_<list>_posts")
        data = m.fetch_page(m.load_token(), TEST_<OWNER>, "")
        if not data: raise unittest.SkipTest("接口异常，跳过")
        items = m._pick(data, "items", "posts", default=[]) or []
        for p in items:
            if (m._safe_int(m._pick(p, "comment_count", "comments_count")) or 0) > 0:
                cls.test_pk = m._pick(p, "code", "id", "pk") or ""
                break
        if not cls.test_pk: raise unittest.SkipTest("无可用测试样本")

    def _run(self, fn, csv_name):
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf): fn(Path(tmp))
            csv_file = Path(tmp) / csv_name
            self.assertTrue(csv_file.exists(), f"未生成 {csv_name}\n{buf.getvalue()}")
            self.assertGreater(csv_file.stat().st_size, 0)

    def test_get_<list>_posts(self):
        m = _load("get_<list>_posts")
        def runner(tmp):
            with patch.object(sys, "argv", ["x", TEST_<OWNER>,
                    "--output-dir", str(tmp), "--workers", "1", "--max-pages", "1"]):
                m.main()
        self._run(runner, "<prefix>_posts.csv")

    def test_get_<entity>_comments(self):
        m = _load("get_<entity>_comments")
        def runner(tmp):
            with patch.object(sys, "argv", ["x", self.test_pk,
                    "--output-dir", str(tmp), "--max-top", "1", "--no-replies"]):
                m.main()
        self._run(runner, "<prefix>_comments.csv")

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

要点：

- `setUpClass` 动态拿测试样本，避免硬编码 ID 失效
- `--max-pages 1 / --max-top 1 / --no-replies` 把配额消耗压到最小
- `redirect_stdout(io.StringIO())` 捕获脚本日志，失败时一并打印
- 运行：`python3 skills/<platform>-justoneapi/tests/test_scripts_smoke.py`
- **`.env` 必须有 `JUSTONEAPI_TOKEN`**（仓库根目录），否则 setUpClass 会 SkipTest

