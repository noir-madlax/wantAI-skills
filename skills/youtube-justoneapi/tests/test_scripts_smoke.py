#!/usr/bin/env python3
"""scripts/ 采集脚本的冒烟测试（mock 外部 HTTP，使用 respJson 样例数据）。

策略：
  - mock JustOneAPI 请求（_request）：返回 respJson/ 目录下的离线样例，不消耗配额。
  - mock 后端 upsert（upload_to_backend）：直接返回 True，不依赖后端服务。
  - mock load_token：返回占位 token，不依赖 .env 文件。
  - 校验：CSV 正常生成、行数、关键字段。
"""
import csv
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPTS_DIR  = Path(__file__).resolve().parent.parent / "scripts"
RESP_DIR     = Path(__file__).resolve().parent.parent / "respJson"

# 离线样例
RESP_CHANNEL_VIDEOS = json.loads((RESP_DIR / "get-channel-videos.json").read_text())
RESP_VIDEO_COMMENT  = json.loads((RESP_DIR / "get-video-comment.json").read_text())
RESP_SUB_COMMENT    = json.loads((RESP_DIR / "get-video-sub-comment.json").read_text())

# 测试参数（与 respJson 对应）
TEST_CHANNEL_ID = "UCe0TLA0EsQbE-MjuHXevj2A"          # 请求参数，不在响应里
TEST_VIDEO_ID   = "1uu4E8xtY7M"                        # 顶层/子评论均属该视频


def _load(name: str):
    """把 scripts/<name>.py 作为独立模块加载（隔离全局状态）。"""
    path = SCRIPTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_yt_test_{name}", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestGetChannelVideos(unittest.TestCase):
    """get_channel_videos.py 冒烟测试。"""

    def _make_request_side_effect(self):
        """首页返回样例数据（含 continuation_token），第二次返回空（终止翻页）。"""
        calls = []
        def side_effect(token, params):
            calls.append(params)
            if len(calls) == 1:
                return RESP_CHANNEL_VIDEOS["data"]
            return {"videos": [], "continuation_token": None}
        return side_effect

    def test_csv_generated_with_correct_rows(self):
        mod = _load("get_channel_videos")

        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with patch.object(mod, "load_token", return_value="fake_token"), \
                 patch.object(mod, "_request",        side_effect=self._make_request_side_effect()), \
                 patch.object(mod, "upload_to_backend", return_value=True), \
                 patch.object(sys, "argv", ["get_channel_videos.py", TEST_CHANNEL_ID,
                                            "--output-dir", tmp, "--max-pages", "1"]):
                with redirect_stdout(buf):
                    mod.main()

            csv_file = Path(tmp) / "yt_videos.csv"
            self.assertTrue(csv_file.exists(), "yt_videos.csv 未生成")
            csv.field_size_limit(1024 * 1024)
            with open(csv_file, encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))

            expected_count = len(RESP_CHANNEL_VIDEOS["data"]["videos"])
            self.assertGreaterEqual(len(rows), expected_count,
                                    f"行数 {len(rows)} 少于预期 {expected_count}")

    def test_row_fields(self):
        """校验首行关键字段正确写入。"""
        mod = _load("get_channel_videos")

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(mod, "load_token", return_value="fake_token"), \
                 patch.object(mod, "_request", side_effect=self._make_request_side_effect()), \
                 patch.object(mod, "upload_to_backend", return_value=True), \
                 patch.object(sys, "argv", ["get_channel_videos.py", TEST_CHANNEL_ID,
                                            "--output-dir", tmp]):
                with redirect_stdout(io.StringIO()):
                    mod.main()

            with open(Path(tmp) / "yt_videos.csv", encoding="utf-8-sig") as fp:
                row = next(csv.DictReader(fp))

            self.assertEqual(row["channel_id"], TEST_CHANNEL_ID)
            self.assertTrue(row["video_id"],   "video_id 为空")
            self.assertTrue(row["title"],       "title 为空")
            self.assertTrue(row["raw_data"],    "raw_data 为空")
            # view_count 应为纯整数
            self.assertTrue(row["view_count"].isdigit(), f"view_count 非纯整数: {row['view_count']!r}")

    def test_dedup_on_rerun(self):
        """同一 channel 连续跑两次，第二次不重复写入。"""
        mod = _load("get_channel_videos")

        call_n = [0]
        def _req(token, params):
            call_n[0] += 1
            return RESP_CHANNEL_VIDEOS["data"] if call_n[0] == 1 else {"videos": []}

        with tempfile.TemporaryDirectory() as tmp:
            kwargs = dict(
                mod=mod, channel_id=TEST_CHANNEL_ID, tmp=tmp, req_fn=_req
            )
            def run_once():
                call_n[0] = 0
                with patch.object(mod, "load_token", return_value="fake_token"), \
                     patch.object(mod, "_request", side_effect=_req), \
                     patch.object(mod, "upload_to_backend", return_value=True), \
                     patch.object(sys, "argv", ["get_channel_videos.py", TEST_CHANNEL_ID,
                                                "--output-dir", tmp]):
                    with redirect_stdout(io.StringIO()):
                        mod.main()

            run_once()
            csv_file = Path(tmp) / "yt_videos.csv"
            with open(csv_file, encoding="utf-8-sig") as fp:
                count_first = sum(1 for _ in csv.DictReader(fp))

            run_once()
            with open(csv_file, encoding="utf-8-sig") as fp:
                count_second = sum(1 for _ in csv.DictReader(fp))

            self.assertEqual(count_first, count_second, "二次运行产生重复行")


class TestGetVideoComments(unittest.TestCase):
    """get_video_comments.py 冒烟测试。"""

    def _make_request_side_effect(self, include_sub=True):
        """首次返回顶层评论，子评论请求返回 sub-comment 样例，后续翻页终止。"""
        top_done   = [False]
        sub_called = {}

        def side_effect(token, endpoint, params):
            if "sub-comment-list" in endpoint:
                # 子评论 endpoint 优先判断（它同样包含 "comment-list"）
                pass
            elif "comment-list" in endpoint:
                if not top_done[0]:
                    top_done[0] = True
                    return RESP_VIDEO_COMMENT["data"]
                return {"comments": [], "continuation_token": None}
            # sub-comment endpoint
            cid = params.get("commentId", "")
            if cid not in sub_called:
                sub_called[cid] = True
                return RESP_SUB_COMMENT["data"] if include_sub else {"comments": []}
            return {"comments": [], "continuation_token": None}

        return side_effect

    def test_top_comments_csv(self):
        mod = _load("get_video_comments")

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(mod, "load_token", return_value="fake_token"), \
                 patch.object(mod, "_request",         side_effect=self._make_request_side_effect()), \
                 patch.object(mod, "upload_to_backend", return_value=True), \
                 patch.object(sys, "argv", ["get_video_comments.py", TEST_VIDEO_ID,
                                            "--output-dir", tmp, "--no-replies"]):
                with redirect_stdout(io.StringIO()):
                    mod.main()

            csv_file = Path(tmp) / "yt_comments.csv"
            self.assertTrue(csv_file.exists(), "yt_comments.csv 未生成")
            csv.field_size_limit(1024 * 1024)
            with open(csv_file, encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))

            expected = len(RESP_VIDEO_COMMENT["data"]["comments"])
            self.assertGreaterEqual(len(rows), expected)
            # 全部是顶层评论
            self.assertTrue(all(r["is_sub"] == "0" for r in rows), "存在子评论行")

    def test_sub_comments_included(self):
        """不加 --no-replies 时，子评论也应落 CSV。"""
        mod = _load("get_video_comments")

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(mod, "load_token", return_value="fake_token"), \
                 patch.object(mod, "_request",         side_effect=self._make_request_side_effect(include_sub=True)), \
                 patch.object(mod, "upload_to_backend", return_value=True), \
                 patch.object(sys, "argv", ["get_video_comments.py", TEST_VIDEO_ID,
                                            "--output-dir", tmp]):
                with redirect_stdout(io.StringIO()):
                    mod.main()

            csv.field_size_limit(1024 * 1024)
            with open(Path(tmp) / "yt_comments.csv", encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))

            sub_rows = [r for r in rows if r["is_sub"] == "1"]
            self.assertGreater(len(sub_rows), 0, "未写入任何子评论行")
            # 子评论的 root_comment_id 应能在顶层评论的 comment_id 中找到
            top_ids = {r["comment_id"] for r in rows if r["is_sub"] == "0"}
            for r in sub_rows:
                self.assertIn(r["root_comment_id"], top_ids,
                              f"子评论 root_comment_id={r['root_comment_id']!r} 无对应顶层评论")

    def test_row_video_id_populated(self):
        """每行 video_id 应等于入参。"""
        mod = _load("get_video_comments")

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(mod, "load_token", return_value="fake_token"), \
                 patch.object(mod, "_request",         side_effect=self._make_request_side_effect()), \
                 patch.object(mod, "upload_to_backend", return_value=True), \
                 patch.object(sys, "argv", ["get_video_comments.py", TEST_VIDEO_ID,
                                            "--output-dir", tmp]):
                with redirect_stdout(io.StringIO()):
                    mod.main()

            csv.field_size_limit(1024 * 1024)
            with open(Path(tmp) / "yt_comments.csv", encoding="utf-8-sig") as fp:
                rows = list(csv.DictReader(fp))

            for r in rows:
                self.assertEqual(r["video_id"], TEST_VIDEO_ID,
                                 f"comment_id={r['comment_id']} 的 video_id 错误")


if __name__ == "__main__":
    unittest.main(verbosity=2)
