"""
test_basic.py
"""

import tempfile
import unittest
from unittest.mock import MagicMock, patch

from googleapiclient.errors import HttpError

from pytubekit.constants import NEXT_PAGE_TOKEN, ITEMS_TOKEN, DELETED_TITLE, PRIVATE_TITLE
from pytubekit.util import (
    PagedRequest, get_playlist_ids_from_names, cleanup_items,
    retry_execute, read_video_ids_from_files, log_progress,
)


def _make_item(video_id: str, title: str = "Title", item_id: str | None = None) -> dict:
    if item_id is None:
        item_id = f"item_{video_id}"
    return {
        "id": item_id,
        "snippet": {
            "title": title,
            "resourceId": {"videoId": video_id},
        },
    }


def _make_playlist_item(playlist_id: str, title: str) -> dict:
    return {
        "id": playlist_id,
        "snippet": {"title": title},
    }


class TestPagedRequestSinglePage(unittest.TestCase):
    def test_single_page(self):
        items = [_make_item("v1"), _make_item("v2")]
        mock_f = MagicMock(return_value=MagicMock(
            execute=MagicMock(return_value={ITEMS_TOKEN: items}),
        ))
        pr = PagedRequest(f=mock_f, kwargs={"part": "snippet"})
        result = pr.get_all_items()
        self.assertEqual(result, items)
        mock_f.assert_called_once_with(part="snippet")

    def test_multi_page(self):
        page1_items = [_make_item("v1")]
        page2_items = [_make_item("v2")]
        responses = [
            {ITEMS_TOKEN: page1_items, NEXT_PAGE_TOKEN: "token2"},
            {ITEMS_TOKEN: page2_items},
        ]
        call_count = 0

        def mock_f_call(**_kwargs):
            nonlocal call_count
            resp = responses[call_count]
            call_count += 1
            mock_req = MagicMock()
            mock_req.execute.return_value = resp
            return mock_req

        pr = PagedRequest(f=mock_f_call, kwargs={"part": "snippet"})
        result = pr.get_all_items()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["snippet"]["resourceId"]["videoId"], "v1")
        self.assertEqual(result[1]["snippet"]["resourceId"]["videoId"], "v2")

    def test_empty_page(self):
        mock_f = MagicMock(return_value=MagicMock(
            execute=MagicMock(return_value={ITEMS_TOKEN: []}),
        ))
        pr = PagedRequest(f=mock_f, kwargs={})
        result = pr.get_all_items()
        self.assertEqual(result, [])


class TestGetPlaylistIdsFromNames(unittest.TestCase):
    @patch("pytubekit.util.create_playlists_request")
    def test_lookup(self, mock_create):
        mock_pr = MagicMock()
        mock_pr.get_all_items.return_value = [
            _make_playlist_item("id_a", "Playlist A"),
            _make_playlist_item("id_b", "Playlist B"),
        ]
        mock_create.return_value = mock_pr
        youtube = MagicMock()
        result = get_playlist_ids_from_names(youtube, ["Playlist B", "Playlist A"])
        self.assertEqual(result, ["id_b", "id_a"])

    @patch("pytubekit.util.create_playlists_request")
    def test_missing_name_raises(self, mock_create):
        mock_pr = MagicMock()
        mock_pr.get_all_items.return_value = [
            _make_playlist_item("id_a", "Playlist A"),
        ]
        mock_create.return_value = mock_pr
        youtube = MagicMock()
        with self.assertRaises(KeyError):
            get_playlist_ids_from_names(youtube, ["No Such Playlist"])


class TestCleanupItems(unittest.TestCase):
    def _run_cleanup(self, items, *, dedup=False, check_deleted=False, check_privatized=False, do_delete=True):
        youtube = MagicMock()
        cleanup_items(
            youtube, items,
            dedup=dedup,
            check_deleted=check_deleted,
            check_privatized=check_privatized,
            do_delete=do_delete,
        )
        return youtube

    def test_dedup_removes_second_occurrence(self):
        items = [_make_item("v1", item_id="i1"), _make_item("v1", item_id="i2")]
        youtube = self._run_cleanup(items, dedup=True)
        youtube.playlistItems().delete.assert_called_once_with(id="i2")

    def test_dedup_keeps_unique(self):
        items = [_make_item("v1", item_id="i1"), _make_item("v2", item_id="i2")]
        youtube = self._run_cleanup(items, dedup=True)
        youtube.playlistItems().delete.assert_not_called()

    def test_deleted_detection(self):
        items = [_make_item("v1", title=DELETED_TITLE, item_id="i1"), _make_item("v2", item_id="i2")]
        youtube = self._run_cleanup(items, check_deleted=True)
        youtube.playlistItems().delete.assert_called_once_with(id="i1")

    def test_private_detection(self):
        items = [_make_item("v1", title=PRIVATE_TITLE, item_id="i1")]
        youtube = self._run_cleanup(items, check_privatized=True)
        youtube.playlistItems().delete.assert_called_once_with(id="i1")

    def test_do_delete_false_skips_api_call(self):
        items = [_make_item("v1", title=DELETED_TITLE, item_id="i1")]
        youtube = self._run_cleanup(items, check_deleted=True, do_delete=False)
        youtube.playlistItems().delete.assert_not_called()

    def test_no_flags_deletes_nothing(self):
        items = [_make_item("v1", title=DELETED_TITLE, item_id="i1")]
        youtube = self._run_cleanup(items)
        youtube.playlistItems().delete.assert_not_called()


class TestRetryExecute(unittest.TestCase):
    def test_success_first_try(self):
        request = MagicMock()
        request.execute.return_value = {"ok": True}
        result = retry_execute(request)
        self.assertEqual(result, {"ok": True})
        request.execute.assert_called_once()

    @patch("pytubekit.util.time.sleep")
    def test_retry_on_429(self, mock_sleep):
        resp = MagicMock()
        resp.status = 429
        error = HttpError(resp, b"rate limited")
        request = MagicMock()
        request.execute.side_effect = [error, {"ok": True}]
        result = retry_execute(request, max_retries=3)
        self.assertEqual(result, {"ok": True})
        self.assertEqual(request.execute.call_count, 2)
        mock_sleep.assert_called_once_with(1)

    @patch("pytubekit.util.time.sleep")
    def test_non_retryable_error_raises_immediately(self, mock_sleep):
        resp = MagicMock()
        resp.status = 404
        error = HttpError(resp, b"not found")
        request = MagicMock()
        request.execute.side_effect = error
        with self.assertRaises(HttpError):
            retry_execute(request, max_retries=3)
        request.execute.assert_called_once()
        mock_sleep.assert_not_called()

    @patch("pytubekit.util.time.sleep")
    def test_all_retries_exhausted(self, _mock_sleep):
        resp = MagicMock()
        resp.status = 503
        error = HttpError(resp, b"service unavailable")
        request = MagicMock()
        request.execute.side_effect = error
        with self.assertRaises(HttpError):
            retry_execute(request, max_retries=3)
        self.assertEqual(request.execute.call_count, 3)


class TestReadVideoIdsFromFiles(unittest.TestCase):
    def test_reads_ids(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("abc123\n\ndef456\nabc123\n")
            path = f.name
        result = read_video_ids_from_files([path])
        self.assertEqual(result, {"abc123", "def456"})

    def test_multiple_files(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f1:
            f1.write("id1\n")
            path1 = f1.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f2:
            f2.write("id2\n")
            path2 = f2.name
        result = read_video_ids_from_files([path1, path2])
        self.assertEqual(result, {"id1", "id2"})

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            path = f.name
        result = read_video_ids_from_files([path])
        self.assertEqual(result, set())


class TestLogProgress(unittest.TestCase):
    def test_logs_at_interval(self):
        logger = MagicMock()
        log_progress(logger, 100, 500, interval=100)
        logger.info.assert_called_once()

    def test_logs_at_total(self):
        logger = MagicMock()
        log_progress(logger, 500, 500, interval=100)
        logger.info.assert_called_once()

    def test_skips_non_interval(self):
        logger = MagicMock()
        log_progress(logger, 50, 500, interval=100)
        logger.info.assert_not_called()
