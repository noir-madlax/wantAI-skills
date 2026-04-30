#!/usr/bin/env python3
"""scripts/ 采集脚本的回归冒烟测试（真实接口调用）。

策略：
  - 不 mock，真实请求 JustOneAPI 与 GoodGame upsert 接口。
  - 入参写死，每个脚本只调一次（max_pages=1）压低配额消耗。
"""
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
TEST_USERNAME = "nasa"
TEST_POST_CODE = "DW6mSqqgcpn"
TEST_POST_MEDIA_ID = "3871575238206671463"


def _load(name: str):
    """把 scripts/<name>.py 作为独立模块加载。"""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_ig_test_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ScriptsSmokeTest(unittest.TestCase):
    """每脚本一个 case：真实端到端跑通即视为回归通过。"""

    def _run(self, fn, csv_name):
        """通用执行器：跑 fn()，校验 CSV 生成。"""
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                fn(Path(tmp))
            tmp_path = Path(tmp)
            csv_file = tmp_path / csv_name
            self.assertTrue(csv_file.exists(),
                            f"未生成 {csv_name}: {list(tmp_path.iterdir())}\n"
                            f"--- stdout ---\n{buf.getvalue()}")
            self.assertGreater(csv_file.stat().st_size, 0,
                               f"{csv_name} 为空\n--- stdout ---\n{buf.getvalue()}")

    def test_get_user_posts(self):
        mod = _load("get_user_posts")

        def runner(tmp):
            with patch.object(sys, "argv",
                              ["get_user_posts.py", TEST_USERNAME,
                               "--output-dir", str(tmp),
                               "--workers", "1", "--max-pages", "1"]):
                mod.main()
        self._run(runner, "ig_posts.csv")

    def test_get_post_comments(self):
        mod = _load("get_post_comments")
        entry = f"{TEST_POST_CODE}:{TEST_POST_MEDIA_ID}"

        def runner(tmp):
            with patch.object(sys, "argv",
                              ["get_post_comments.py", entry,
                               "--output-dir", str(tmp),
                               "--max-top", "10", "--no-replies"]):
                mod.main()
        self._run(runner, "ig_post_comments.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
