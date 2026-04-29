#!/usr/bin/env python3
"""scripts/ 4 个采集脚本的回归冒烟测试。

设计目标：每次改完代码跑一次，确认 4 个脚本端到端不抛异常、能正确生成 CSV。

策略：
  - 不访问真实的 JustOneAPI / GoodGame 后端，全部 mock。
  - 用 importlib 把每个脚本作为模块加载，再 patch 该模块内的 requests / load_token。
  - 每个脚本一个 test case：构造最小可用响应，跑完一轮翻页（has_more=False / max_pages=1）即结束。

运行：
  python skills/xiaohongshu-justoneapi/tests/test_scripts_smoke.py
  python -m unittest skills.xiaohongshu-justoneapi.tests.test_scripts_smoke
"""
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    """把 scripts/<name>.py 作为独立模块加载。"""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_xhs_test_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _resp(payload: dict, status: int = 200) -> MagicMock:
    """构造一个最小可用的 requests.Response mock。"""
    r = MagicMock()
    r.status_code = status
    r.headers = {"content-type": "application/json"}
    r.json.return_value = payload
    r.raise_for_status.return_value = None
    return r


# ── Mock fixtures ─────────────────────────────────────────────────
USER_ITEM = {
    "id": "u1", "red_id": "r1", "name": "测试用户", "desc": "bio",
    "sub_title": "sub", "red_official_verified": True,
    "red_official_verify_type": 1, "image": "img.jpg", "link": "https://x",
}
NOTE_ITEM = {
    "id": "n1", "type": "normal", "timestamp": 1700000000,
    "title": "t", "desc": "d",
    "user": {"userid": "u1", "nickname": "n", "red_id": "r1"},
    "liked_count": 1, "comments_count": 2,
    "collected_count": 3, "shared_count": 4,
    "images_list": [{"url": "https://example.com/x.jpg"}],
}
USER_NOTE_ITEM = {
    "id": "n1", "create_time": 1700000000, "title": "t", "desc": "d",
    "type": "normal", "sticky": False,
    "user": {"userid": "u1", "nickname": "n"},
    "likes": "10", "comments_count": "2",
    "collected_count": "3", "share_count": "1",
    "images_list": [{"url": "https://example.com/x.jpg"}],
    "cursor": "c1",
}
COMMENT_ITEM = {
    "id": "c1", "content": "hi", "time": 1700000000,
    "comment_type": 1, "like_count": 5, "sub_comment_count": 0,
    "status": 0, "ip_location": "上海",
    "user": {"userid": "u1", "nickname": "n", "red_id": "r1", "images": "a"},
    "pictures": [],
}
UPLOAD_OK = {"code": 0, "data": {"count": 1}}


class ScriptsSmokeTest(unittest.TestCase):
    """每脚本一个 case：mock 网络后端到端跑通即视为回归通过。"""

    def _run(self, mod, fn, get_payload, list_glob_or_name):
        """通用执行器：patch token + requests，跑 fn()，校验输出。"""
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(mod, "load_token", return_value="fake-token"), \
                patch.object(mod.requests, "get",
                             return_value=_resp(get_payload)), \
                patch.object(mod.requests, "post",
                             return_value=_resp(UPLOAD_OK)) as post, \
                redirect_stdout(io.StringIO()):
            fn(Path(tmp))
            tmp_path = Path(tmp)
            if callable(list_glob_or_name):
                self.assertTrue(list_glob_or_name(tmp_path),
                                f"未生成预期 CSV: {list(tmp_path.iterdir())}")
            else:
                self.assertTrue((tmp_path / list_glob_or_name).exists(),
                                f"未生成 {list_glob_or_name}")
            post.assert_called()  # 必上传

    def test_search_users(self):
        mod = _load("search_users")
        payload = {"code": 0, "data": {"users": [USER_ITEM]}}
        self._run(mod,
                  lambda tmp: mod.crawl("kw", 1, tmp),
                  payload,
                  lambda p: any(p.glob("xhs_users_*.csv")))

    def test_search_notes(self):
        mod = _load("search_notes")
        payload = {"code": 0,
                   "data": {"items": [{"model_type": "note", "note": NOTE_ITEM}]}}
        self._run(mod,
                  lambda tmp: mod.crawl("kw", 1, "general", "_0", tmp),
                  payload,
                  lambda p: any(p.glob("xhs_notes_*.csv")))

    def test_get_user_posts(self):
        mod = _load("get_user_posts")
        payload = {"code": 0,
                   "data": {"notes": [USER_NOTE_ITEM], "has_more": False}}

        def runner(tmp):
            with patch.object(sys, "argv",
                              ["get_user_posts.py", "uid1",
                               "--output-dir", str(tmp), "--workers", "1"]):
                mod.main()
        self._run(mod, runner, payload, "xhs_posts.csv")

    def test_get_note_comments(self):
        mod = _load("get_note_comments")
        payload = {"code": 0,
                   "data": {"comments": [COMMENT_ITEM], "has_more": False}}

        def runner(tmp):
            with patch.object(sys, "argv",
                              ["get_note_comments.py", "nid1",
                               "--output-dir", str(tmp), "--no-replies"]):
                mod.main()
        self._run(mod, runner, payload, "xhs_comments.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
