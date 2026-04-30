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

按顺序走 6 步，**每一步都先与用户确认再继续**，不要跳步。

### 1. 需求 & 接口映射（必须先问）
- 读用户给的 JustOneAPI 文档链接，挑出本次要做的 endpoint
- 输出一张映射表：`用户意图 / endpoint / 必填参数 / 翻页参数`
- 列出待确认问题：排序默认值？并发？特殊 ID 形态（如 IG 的 code vs media_id）？
- **后端 upsert 是默认必备能力，不要再问用户"是否需要"**，直接按规范实现

### 2. DDL 设计（必须用户确认）
- 表前缀统一 `gg_skill_<platform>_`（如 `gg_skill_ig_posts`、`gg_skill_xhs_note_comments`）
- 业务主键用平台原生 ID 做 UNIQUE（小红书 `note_id`、IG `code`）
- 子评论用 `(主键, comment_id)` 复合 UNIQUE，附 `is_sub / parent_comment_id / root_comment_id` 三件套
- 必备列：`raw_data JSONB`（兜底新字段）、`created_at / updated_at TIMESTAMPTZ`、共享 `set_updated_at` 触发器
- 详见 [conventions.md → DDL](./conventions.md#supabase-ddl-模板)

### 3. 后端 upsert 接口（强制对接，等用户给路由路径）
- **不要询问"要不要 upsert"**，每个采集脚本都必须 upsert，这是硬性规范
- 路径约定：`POST https://www.goodgame.monster/api/skill/<platform>/<resource>/upsert`
- 请求体：`{trace_id, items: [...]}`，响应 `{code: 0, data: {count}}`
- 等用户告知 router 文件路径后 `view` 一遍 schema 确认字段名，再写 `UPLOAD_FIELD_MAP`

### 4. 文档落盘（按顺序）
1. `SKILL.md` —— 复制 xhs/ig 同名文件，替换平台名 / 接口表 / 运行示例
2. `apis/<endpoint>.md` —— 一接口一份，含请求 / 响应 / 字段表 / 翻页规则
3. `scripts/<endpoint>.py` —— 复用 [conventions.md → 脚本模板](./conventions.md#脚本结构) 的两种范式

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
