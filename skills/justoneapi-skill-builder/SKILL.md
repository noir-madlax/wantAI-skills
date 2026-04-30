---
name: justoneapi-skill-builder
description: 当用户需要在本仓库新建一个基于 JustOneAPI 的数据采集 skill（接入小红书/Instagram/TikTok/X/YouTube/Facebook 等任意平台的任意接口）时触发。提供标准目录结构、设计 Q&A 工作流、Token / 错误码 / 重试 / 分页 / 断点续传 / 后端 upsert / Supabase DDL / 真实接口冒烟测试的统一规范，确保新 skill 与 xiaohongshu-justoneapi、instagram-justoneapi 风格一致。
---

# JustOneAPI Skill Builder —— 新平台接入元规范

接到用户"按 xxx skill 的格式做一个新平台/新接口"的需求时，**先按 [工作流](#工作流) 走完确认环节，再按 [conventions.md](./conventions.md) 落代码**，全程参照 [参考实现](#参考实现) 中现成的两个 skill。

## 何时触发

任意以下场景：

- 用户给出一个 `https://docs.justoneapi.com/zh/api/<platform>/...` 文档链接，要求"按 xxx 的格式做"
- 用户说"接入 X 平台的 Y 接口"、"做一个 Z 平台的采集 skill"
- 用户已有 `skills/<some-platform>-justoneapi/` 想新增接口或扩展为新平台

## 标准目录结构

每个新 skill 必须落在 `skills/<platform>-justoneapi/`，结构与 xhs / ig 完全对齐：

```
skills/<platform>-justoneapi/
├── SKILL.md                        # 入口：frontmatter + token + 错误码 + ID 速查 + 接口目录 + 运行示例
├── apis/
│   └── <endpoint>.md               # 每个接口一份独立文档
├── scripts/
│   └── <endpoint>.py               # 每个接口一份独立 uv 脚本（PEP 723 头）
└── tests/
    └── test_scripts_smoke.py       # 真实调接口的冒烟测试，每脚本 1 个 case
```

## 工作流

按顺序走 6 步。**全流程只有 [步骤 2 DDL] 一处需要用户确认**，其余环节（含后端 upsert）全部由 agent 自行实现，不要等用户。

### 1. 需求 & 接口映射（自助产出，无需确认）
- 读用户给的 JustOneAPI 文档链接，挑出本次要做的 endpoint
- 输出一张映射表：`用户意图 / endpoint / 必填参数 / 翻页参数`
- 默认决策（不要再问）：排序取文档默认值；并发列表型 3 / 评论型 1；后端 upsert **必接**

### 2. DDL 设计（**唯一需用户确认的环节**）
- 输出 Supabase DDL 草案后**显式问用户**："DDL 没问题的话我直接执行并继续后续实现"
- 表前缀统一 `gg_skill_<platform>_`（如 `gg_skill_ig_posts`、`gg_skill_xiaohongshu_note_comments`）
- 业务主键用平台原生 ID 做 UNIQUE（小红书 `note_id`、IG `code`）
- 子评论用 `(主键, comment_id)` 复合 UNIQUE，附 `is_sub / parent_comment_id / root_comment_id` 三件套
- 必备列：`raw_data JSONB`、`created_at / updated_at TIMESTAMPTZ`、共享 `set_updated_at` 触发器
- 用户确认后用 supabase 工具直接执行；详见 [conventions.md → DDL](./conventions.md#supabase-ddl-模板)

### 3. 后端 upsert 实现（**agent 自助实现，不要等用户**）
GoodGame 后端仓库位于 `/Users/noir/Projects/GoodGame/`，按下表 6 个文件分层落盘，**全部仿照 `xiaohongshu` 实现**（具体路径与代码模式见 [conventions.md → 后端文件分层](./conventions.md#后端文件分层规范)）：

| # | 文件 | 职责 |
|---|------|------|
| 1 | `backend/KOL/orm/skill/<platform>_models.py` | Pydantic Model，字段对齐 Supabase 表 |
| 2 | `backend/KOL/orm/skill/<platform>_repositories.py` | Repository 类：`TABLE` / `ON_CONFLICT` / `bulk_upsert` / `upsert` / `get_by_xxx` / `_row_to_model` |
| 3 | `backend/KOL/orm/skill/__init__.py` | 导出新增 Models 和 Repositories |
| 4 | `backend/api/schemas/skill_data_<platform>.py` | `<X>UpsertItem` / `<X>UpsertRequest(BaseRequest)` / `<X>UpsertResult` / `<X>Ref`（复合键时） |
| 5 | `backend/api/routers/skill_data_<platform>.py` | `router = APIRouter()` + `@router.post("/skill/<platform>/<resource>/upsert", ...)` |
| 6 | `backend/api/server.py` | `from .routers import ... <platform>...` + `app.include_router(<platform>.router, prefix="/api", tags=["skill-<platform>"])` |

> 实现完直接进入步骤 4，无需提交后端 PR，也不用问用户 "后端好了吗"。

### 4. Skill 文档与脚本落盘（按顺序）
1. `SKILL.md` —— 复制 xhs/ig 同名文件，替换平台名 / 接口表 / 运行示例
2. `apis/<endpoint>.md` —— 一接口一份，含请求 / 响应 / 字段表 / 翻页规则
3. `scripts/<endpoint>.py` —— 复用 [conventions.md → 脚本结构](./conventions.md#脚本结构) 的两种范式
4. `UPLOAD_FIELD_MAP` 直接对齐步骤 3 写好的 schema 字段名

### 5. 真实接口冒烟测试（不要 mock）
- 参考 `skills/instagram-justoneapi/tests/test_scripts_smoke.py`
- 用 `setUpClass` 调一次列表接口动态拿一个稳定的业务 ID 给评论测试用，避免硬编码失效
- 限制 `max_pages=1 / max_top=1 / --no-replies` 把配额消耗压到最小
- **必须真实命中 JustOneAPI + GoodGame 后端**，跑一次确保 CSV 生成 + 后端返回 `code=0`

### 6. 字段兜底回归
- 真实响应字段名常与文档不一致（如 IG `data.data.items` 嵌套、`pk` vs `id`、`comment_like_count` vs `like_count`）
- 用 `_pick(d, *keys, default=None)` 多名兜底；新发现的别名加进 `_pick` 候选列表
- 详见 [conventions.md → 字段兜底](./conventions.md#字段名兜底)

## 参考实现

任何疑问优先看这两个现成 skill —— 它们是**活模板**，直接 copy-adapt 即可：

| 平台 | 路径 | 包含范式 |
|------|------|----------|
| 小红书 | `skills/xiaohongshu-justoneapi/` | 4 个脚本：搜索用户 / 搜索笔记 / 用户笔记 / 笔记评论；多线程 + 评论两阶段 |
| Instagram | `skills/instagram-justoneapi/` | 2 个脚本：用户帖子 / 帖子评论；含 ID 二义性处理（`code:media_id`） |

## 终检清单

提交前逐项核对，缺一不可：

- [ ] `SKILL.md` 含 YAML frontmatter（`name` + 触发场景丰富的 `description`）
- [ ] `SKILL.md` 含错误码表（直接复制 conventions.md 的版本）
- [ ] `SKILL.md` 含 `## 数据落地` 段，列明 `*_progress.json` / `*_failed.jsonl` 的语义
- [ ] 每个 `scripts/*.py` 都有 PEP 723 头（`# /// script ... # ///`）
- [ ] `load_token()` 函数与 conventions.md 完全一致（不要改）
- [ ] CSV 含 `raw_json` / `raw_data` 列保留原始响应
- [ ] 进度文件命名：`.<prefix>_<type>_progress.json`（开头点号，被 git 忽略）
- [ ] 失败文件命名：`<prefix>_<type>_failed.jsonl`
- [ ] **每个采集脚本都接入了后端 upsert**（强制项，不存在"不需要后端"的脚本）
- [ ] 后端 upsert 顺序：**先 upload，再写 CSV**（避免 CSV 写完崩了导致下次跳过）
- [ ] `tests/test_scripts_smoke.py` 真实调通过（`python3 tests/test_scripts_smoke.py` 全绿）
- [ ] 根 `README.md` 的 Skills 列表新增一行
- [ ] **不要**自行创建额外 `*.md` 文档（README / CHANGELOG / TESTING 等），SKILL.md + apis/ 已经够了
