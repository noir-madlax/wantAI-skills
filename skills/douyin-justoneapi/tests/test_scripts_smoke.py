#!/usr/bin/env python3
"""scripts/ 采集脚本的回归冒烟测试（真实接口调用）。

策略：
  - 不 mock，真实请求 JustOneAPI 与 GoodGame upsert 接口。
  - 入参写死，每个脚本只调一次（max_pages=1 / max_top 极小）压低配额消耗。
"""
import csv
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

# TODO: 由用户填入真实测试数据
TEST_SEC_UID = "MS4wLjABAAAAZAbWtk65P5pcQzjwNBKSDfidHBcZCJfAwLkCGjNkokk"    # 抖音用户 sec_uid，形如 MS4wLjABAAAA...
TEST_AWEME_ID = "7632183372408211700"   # 抖音视频 aweme_id，形如 7300000000000000000


def _load(name: str):
    """把 scripts/<name>.py 作为独立模块加载。"""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_dy_test_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ScriptsSmokeTest(unittest.TestCase):
    """每脚本一个 case：真实端到端跑通即视为回归通过。"""

    def _run(self, fn, csv_name, min_rows: int = 1):
        """通用执行器：跑 fn()，校验 CSV 生成且至少包含 min_rows 条数据。"""
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                fn(Path(tmp))
            tmp_path = Path(tmp)
            csv_file = tmp_path / csv_name
            stdout = buf.getvalue()
            self.assertTrue(csv_file.exists(),
                            f"未生成 {csv_name}: {list(tmp_path.iterdir())}\n"
                            f"--- stdout ---\n{stdout}")
            csv.field_size_limit(1024 * 1024)
            with open(csv_file, encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))
            self.assertGreaterEqual(len(rows), min_rows,
                                    f"{csv_name} 仅 {len(rows)} 条数据，期望至少 {min_rows} 条\n"
                                    f"--- stdout ---\n{stdout}")

    @unittest.skipUnless(TEST_SEC_UID, "TEST_SEC_UID 未填，跳过")
    def test_get_user_videos(self):
        mod = _load("get_user_videos")

        def runner(tmp):
            with patch.object(sys, "argv",
                              ["get_user_videos.py", TEST_SEC_UID,
                               "--output-dir", str(tmp),
                               "--workers", "1", "--max-pages", "1"]):
                mod.main()
        self._run(runner, "douyin_videos.csv")

    @unittest.skipUnless(TEST_AWEME_ID, "TEST_AWEME_ID 未填，跳过")
    def test_get_video_comments(self):
        mod = _load("get_video_comments")

        def runner(tmp):
            with patch.object(sys, "argv",
                              ["get_video_comments.py", TEST_AWEME_ID,
                               "--output-dir", str(tmp),
                               "--max-top", "5", "--no-replies"]):
                mod.main()
        self._run(runner, "douyin_video_comments.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
