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
| [xiaohongshu-justoneapi](./skills/xiaohongshu-justoneapi/SKILL.md) | 支持搜索用户、获取用户笔记、搜索笔记、获取笔记评论 |
| [instagram-justoneapi](./skills/instagram-justoneapi/SKILL.md) | 支持获取用户帖子、获取帖子评论（含回复） |
| [douyin-justoneapi](./skills/douyin-justoneapi/SKILL.md) | 支持获取用户视频、获取视频评论（含回复） |
| [youtube-justoneapi](./skills/youtube-justoneapi/SKILL.md) | 支持获取频道视频列表、获取视频评论（含子评论） |
| [facebook-rapidapi](./skills/facebook-rapidapi/SKILL.md) | 支持获取主页帖子（含 Reels / 互动数据 / 媒体） |
| [justoneapi-skill-builder](./skills/justoneapi-skill-builder/SKILL.md) | 元规范：当需要新建一个 JustOneAPI 平台 skill 时使用，提供工作流 / 代码规范 / DDL / 测试模板 |
| [social-post-writer](./skills/social-post-writer/SKILL.md) | 根据 brief 与 KOL 信息生成小红书 / Instagram / Facebook 可发布帖子文案 |
| [brand-post-writer](./skills/brand-post-writer/SKILL.md) | 根据品牌人设、产品矩阵、品牌护栏与 brief 生成小红书 / 公众号 / Instagram / Facebook 品牌官方账号帖子文案 |

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
