# wantAI-skills

一个面向 AI 编码助手的可复用 Skill 集合，适用于 **Cursor**、**Augment**、**Claude Code** 等主流 Agent 工具。

## 快速安装

```bash
# 安装全部 skills
npx skills add wantAI/wantAI-skills

# 只安装指定 skill
npx skills add wantAI/wantAI-skills --skill code-review

# 安装到指定 Agent
npx skills add wantAI/wantAI-skills -a cursor -a augment
```

## Skills 列表

| Skill | 描述 |
|-------|------|
| [xiaohongshu-justoneapi](./skills/xiaohongshu-justoneapi/SKILL.md) | 通过 JustOneAPI 采集小红书数据，支持用户搜索、笔记抓取，结果输出为 CSV |

## 目录结构

```
wantAI-skills/
└── skills/
    └── <skill-name>/
        ├── SKILL.md        # Skill 定义文件（含 YAML frontmatter）
        ├── apis/           # 接口文档（可选）
        │   └── <api>.md
        └── scripts/        # 可直接运行的脚本（可选，uv run）
            └── <script>.py
```

## 如何贡献新 Skill

1. 在 `skills/` 目录下新建一个文件夹（名称使用小写连字符格式，如 `my-skill`）
2. 在文件夹内创建 `SKILL.md`，格式如下：

```markdown
---
name: my-skill
description: 简要描述这个 Skill 的功能以及何时触发它（供 Agent 自动选择）
---

# Skill 标题

在这里写给 Agent 的详细指令...
```

3. 提交 PR，描述 Skill 的使用场景和价值。

## 本地调试

```bash
# 从本地目录安装
npx skills add ./

# 查看可用 skills
npx skills add ./ --list
```

## License

MIT
