# /// script
# requires-python = ">=3.9"
# dependencies = ["pandas"]
# ///
# prepare.py —— 舆情数据预处理：将大 CSV/JSON 压缩为适合 Agent 分析的结构化摘要
# 用法：uv run prepare.py <input_file> [--top N] [--output summary.json]
# 示例：uv run prepare.py ./output/xhs_posts.csv --top 30 --output sentiment_summary.json

import argparse, json, sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    sys.exit("❌ 请先安装依赖：pip install pandas  或直接用 uv run 运行")


# ── 字段映射（兼容不同数据源）──────────────────────────────────
FIELD_MAP = {
    # 小红书 (xiaohongshu-justoneapi)
    "xhs": {
        "text":       lambda r: f"{r.get('title','')} {r.get('desc','')}".strip(),
        "engagement": lambda r: (
            _safe_int(r.get("likes")) +
            _safe_int(r.get("comments_count")) +
            _safe_int(r.get("collected_count"))
        ),
        "created_at": lambda r: r.get("create_time_fmt", ""),
        "author":     lambda r: r.get("author_nickname", ""),
        "author_id":  lambda r: r.get("author_userid", ""),
        "likes":      lambda r: _safe_int(r.get("likes")),
        "comments":   lambda r: _safe_int(r.get("comments_count")),
        "collects":   lambda r: _safe_int(r.get("collected_count")),
    },
}


def _safe_int(v) -> int:
    try:
        return int(v or 0)
    except (ValueError, TypeError):
        return 0


def _detect_format(df: pd.DataFrame) -> str:
    """根据列名自动推断数据来源。"""
    cols = set(df.columns)
    if {"title", "desc", "likes", "comments_count"}.issubset(cols):
        return "xhs"
    return "generic"


def _map_row(row: dict, fmt: str) -> dict:
    if fmt == "generic":
        text = str(row.get("text", row.get("content", row.get("body", ""))))
        return {
            "text": text[:500],
            "engagement": _safe_int(row.get("engagement", row.get("likes", 0))),
            "created_at": str(row.get("created_at", row.get("date", ""))),
            "author": str(row.get("author", row.get("nickname", ""))),
            "author_id": str(row.get("author_id", "")),
            "likes": _safe_int(row.get("likes", 0)),
            "comments": _safe_int(row.get("comments", row.get("comments_count", 0))),
            "collects": _safe_int(row.get("collects", row.get("collected_count", 0))),
        }
    mapper = FIELD_MAP[fmt]
    return {
        "text": mapper["text"](row)[:500],
        "engagement": mapper["engagement"](row),
        "created_at": mapper["created_at"](row),
        "author": mapper["author"](row),
        "author_id": mapper["author_id"](row),
        "likes": mapper["likes"](row),
        "comments": mapper["comments"](row),
        "collects": mapper["collects"](row),
    }


def main():
    ap = argparse.ArgumentParser(description="舆情数据预处理：CSV/JSON → 分析摘要 JSON")
    ap.add_argument("input", help="输入文件（.csv 或 .json）")
    ap.add_argument("--top", type=int, default=30, help="每类别保留 top N 条（按互动量，默认 30）")
    ap.add_argument("--output", default="sentiment_summary.json", help="输出文件路径")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        sys.exit(f"❌ 文件不存在：{in_path}")

    # ── 读取数据 ──────────────────────────────────────────────
    if in_path.suffix.lower() == ".json":
        raw = json.loads(in_path.read_text(encoding="utf-8"))
        df = pd.DataFrame(raw if isinstance(raw, list) else [raw])
    else:
        df = pd.read_csv(in_path, encoding="utf-8-sig", dtype=str).fillna("")

    total = len(df)
    print(f"读取 {total} 条记录，格式检测中...")

    fmt = _detect_format(df)
    print(f"数据格式：{fmt}")

    # ── 字段映射 ──────────────────────────────────────────────
    records = [_map_row(row, fmt) for row in df.to_dict("records")]
    df2 = pd.DataFrame(records)
    df2 = df2[df2["text"].str.strip() != ""]       # 去除空正文
    df2 = df2.drop_duplicates(subset=["text"])      # 去重

    # ── 按互动量排序，取 top N ────────────────────────────────
    df2 = df2.sort_values("engagement", ascending=False)
    top_n = args.top
    sampled = df2.head(top_n * 3)                   # 留出余量供 Agent 自行分类

    # ── 统计摘要 ──────────────────────────────────────────────
    summary = {
        "meta": {
            "total_records": total,
            "after_dedup": len(df2),
            "sampled": len(sampled),
            "top_n_per_category": top_n,
            "data_format": fmt,
        },
        "stats": {
            "avg_engagement": round(df2["engagement"].mean(), 1),
            "max_engagement": int(df2["engagement"].max()),
            "date_range": {
                "earliest": df2["created_at"].min(),
                "latest":   df2["created_at"].max(),
            },
            "top_authors": (
                df2.groupby("author_id")["engagement"]
                .sum()
                .nlargest(10)
                .reset_index()
                .rename(columns={"author_id": "id", "engagement": "total_engagement"})
                .merge(
                    df2.drop_duplicates("author_id")[["author_id", "author"]],
                    left_on="id", right_on="author_id", how="left"
                )[["id", "author", "total_engagement"]]
                .to_dict("records")
            ),
        },
        "posts": sampled[["text", "engagement", "likes", "comments", "collects", "created_at", "author"]].to_dict("records"),
    }

    out_path = Path(args.output)
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 摘要已输出 → {out_path}")
    print(f"   总计: {total} 条 → 去重后: {len(df2)} 条 → 采样: {len(sampled)} 条")
    print(f"   平均互动量: {summary['stats']['avg_engagement']}")
    print(f"\n下一步：让 Agent 读取 {out_path} 并运行 sentiment-analysis skill 进行分析")


if __name__ == "__main__":
    main()
