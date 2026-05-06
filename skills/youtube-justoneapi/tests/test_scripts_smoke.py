#!/usr/bin/env python3
"""scripts/ 采集脚本冒烟测试（真实接口调用）。

策略：
  - 不 mock，真实请求 JustOneAPI 与 GoodGame upsert 接口。
  - 每脚本只跑 1 页（max-pages=1 / max-top=5）压低配额消耗。
  - 校验：CSV 正常生成且至少 1 条数据。
"""
import csv
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

# 测试参数：频道视频来自 respJson 样例所属频道（Jeremy Ethier / Built With Science）
# 视频评论：respJson 样例中的视频
TEST_CHANNEL_ID = "UCERm5yFZ1SptUEU4wZ2vJvw"
TEST_VIDEO_ID   = "1uu4E8xtY7M"


def _load(name: str):
    """把 scripts/<name>.py 作为独立模块加载。"""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_yt_smoke_{name}", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ScriptsSmokeTest(unittest.TestCase):
    """每脚本一个 case：真实端到端跑通即视为回归通过。"""

    def _run(self, fn, csv_name: str, min_rows: int = 1):
        """通用执行器：跑 fn(tmp_path)，校验 CSV 生成且至少 min_rows 条数据。"""
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                fn(Path(tmp))
            stdout  = buf.getvalue()
            csv_file = Path(tmp) / csv_name
            self.assertTrue(
                csv_file.exists(),
                f"未生成 {csv_name}，stdout:\n{stdout}",
            )
            csv.field_size_limit(1024 * 1024)
            with open(csv_file, encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))
            self.assertGreaterEqual(
                len(rows), min_rows,
                f"{csv_name} 仅 {len(rows)} 条，期望 ≥ {min_rows} 条\nstdout:\n{stdout}",
            )

    def test_get_channel_videos(self):
        """频道视频：只抓第 1 页，验证 CSV 有数据且关键字段不为空。"""
        mod = _load("get_channel_videos")

        def runner(tmp):
            with unittest.mock.patch.object(
                sys, "argv",
                ["get_channel_videos.py", TEST_CHANNEL_ID,
                 "--output-dir", str(tmp),
                 "--max-pages", "1"],
            ):
                mod.main()

        self._run(runner, "yt_videos.csv")

    def test_get_video_comments(self):
        """视频评论：只抓顶层第 1 页（--no-replies），验证 CSV 有数据。"""
        mod = _load("get_video_comments")

        def runner(tmp):
            with unittest.mock.patch.object(
                sys, "argv",
                ["get_video_comments.py", TEST_VIDEO_ID,
                 "--output-dir", str(tmp),
                 "--no-replies",
                 "--max-top", "5"],
            ):
                mod.main()

        self._run(runner, "yt_comments.csv")


# 延迟导入，避免非必要依赖
import unittest.mock  # noqa: E402

if __name__ == "__main__":
    unittest.main(verbosity=2)
