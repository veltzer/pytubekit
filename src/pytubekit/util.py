"""
util.py
"""

import json
import logging
import sys
import time
from typing import Any, IO

import googleapiclient.discovery
import yt_dlp
from googleapiclient.errors import HttpError
from pygooglehelper import get_credentials, ConfigRequest

from pytubekit.configs import ConfigPagination, ConfigPlaylist
from pytubekit.constants import SCOPES, API_SERVICE_NAME, API_VERSION, NEXT_PAGE_TOKEN, PAGE_TOKEN, ITEMS_TOKEN, \
    DELETED_TITLE, PRIVATE_TITLE
from pytubekit.static import APP_NAME


def log_progress(logger: logging.Logger, current: int, total: int, interval: int = 100) -> None:
    if current % interval == 0 or current == total:
        logger.info(f"progress: {current}/{total}")


def retry_execute(request: Any, max_retries: int = 5) -> dict[str, Any]:
    logger = logging.getLogger()
    last_error = None
    for attempt in range(max_retries):
        try:
            return request.execute()
        except HttpError as e:
            last_error = e
            if e.resp.status in (403, 429, 500, 503) and attempt < max_retries - 1:
                wait = 2 ** attempt
                logger.warning(f"API error {e.resp.status}, retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                raise
    raise last_error  # type: ignore[misc]


class PagedRequest:
    def __init__(self, f: Any, kwargs: dict[str, Any]) -> None:
        self.f = f
        self.next_page_token: str | None = None
        self.kwargs = kwargs

    def get_next_page(self) -> tuple[bool, dict[str, Any]]:
        if self.next_page_token is not None:
            self.kwargs[PAGE_TOKEN] = self.next_page_token
        request = self.f(**self.kwargs)
        response = retry_execute(request)
        if NEXT_PAGE_TOKEN in response:
            self.next_page_token = response[NEXT_PAGE_TOKEN]
            over = False
        else:
            over = True
        return over, response

    def get_all_items(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        while True:
            over, response = self.get_next_page()
            # print(f"got {len(response[ITEMS_TOKEN])} items")
            items.extend(response[ITEMS_TOKEN])
            if over:
                break
        return items


def create_playlists_request(youtube: Any) -> PagedRequest:
    kwargs = {
        "part": "snippet",
        "maxResults": ConfigPagination.page_size,
        "mine": True,
    }
    return PagedRequest(f=youtube.playlists().list, kwargs=kwargs)


def create_playlist_request(youtube: Any, playlist_id: str) -> PagedRequest:
    kwargs = {
        "part": "snippet,id",
        "playlistId": playlist_id,
        "maxResults": ConfigPagination.page_size,
    }
    return PagedRequest(f=youtube.playlistItems().list, kwargs=kwargs)


def get_playlist_ids_from_names(youtube: Any, playlist_names: list[str]) -> list[str]:
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    name_to_id = {item["snippet"]["title"]: item["id"] for item in items}
    return [name_to_id[playlist_name] for playlist_name in playlist_names]


def get_all_items(youtube: Any) -> list[dict[str, Any]]:
    if ConfigPlaylist.name is not None:
        playlist_id = get_playlist_ids_from_names(youtube, [ConfigPlaylist.name])[0]
    else:
        playlist_id = ConfigPlaylist.playlist_id
    return get_all_items_from_playlist_id(youtube, playlist_id)


def get_all_items_from_playlist_id(youtube: Any, playlist_id: str) -> list[dict[str, Any]]:
    return create_playlist_request(youtube, playlist_id=playlist_id).get_all_items()


def get_all_items_from_playlist_ids(youtube: Any, playlist_ids: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for playlist_id in playlist_ids:
        items.extend(get_all_items_from_playlist_id(youtube, playlist_id))
    return items


def delete_playlist_item_by_id(youtube: Any, playlist_item_id: str) -> None:
    logger = logging.getLogger()
    logger.info(f"deleting playlist item [{playlist_item_id}]")
    request = youtube.playlistItems().delete(
        id=playlist_item_id,
    )
    retry_execute(request)


def cleanup_items(youtube: Any, items: list[dict[str, Any]], *, dedup: bool, check_deleted: bool, check_privatized: bool, do_delete: bool) -> None:
    logger = logging.getLogger()
    seen: set[str] = set()
    saw = 0
    found_duplicates = 0
    found_deleted = 0
    found_private = 0
    wanted_to_delete = 0
    deleted = 0
    total = len(items)
    for item in items:
        to_delete = False
        saw += 1
        log_progress(logger, saw, total)
        if dedup:
            f_video_id = item["snippet"]["resourceId"]["videoId"]
            if f_video_id in seen:
                found_duplicates += 1
                to_delete = True
            else:
                seen.add(f_video_id)
        if check_deleted:
            f_title = item["snippet"]["title"]
            if f_title == DELETED_TITLE:
                found_deleted += 1
                to_delete = True
        if check_privatized:
            f_title = item["snippet"]["title"]
            if f_title == PRIVATE_TITLE:
                found_private += 1
                to_delete = True
        if to_delete:
            wanted_to_delete += 1
            if do_delete:
                delete_playlist_item_by_id(youtube, item["id"])
                deleted += 1
    logger.info(f"saw {saw} items")
    if dedup:
        logger.info(f"found_duplicates {found_duplicates} items")
    logger.info(f"found_deleted {found_deleted} items")
    logger.info(f"found_private {found_private} items")
    logger.info(f"wanted_to_delete {wanted_to_delete} items")
    logger.info(f"deleted {deleted} items")


def get_youtube() -> Any:
    ConfigRequest.scopes = SCOPES
    ConfigRequest.app_name = APP_NAME
    credentials = get_credentials()
    youtube = googleapiclient.discovery.build(
        serviceName=API_SERVICE_NAME,
        version=API_VERSION,
        credentials=credentials,
        cache_discovery=False,
    )
    return youtube


def get_video_info(youtube: Any, youtube_id: str) -> dict[str, Any]:
    request = youtube.videos().list(
        part="snippet,status,snippet,contentDetails",
        id=youtube_id,
    )
    return retry_execute(request)


def pretty_print(data: Any, fp: IO[str] = sys.stdout) -> None:
    json.dump(data, fp, indent=4)


def get_youtube_channels(youtube: Any) -> Any:
    return youtube.channels()


def get_youtube_playlists(youtube: Any) -> Any:
    return youtube.playlists()


def get_my_playlists_ids(youtube: Any) -> list[str]:
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    ids = []
    for item in items:
        ids.append(item["id"])
    return ids


def get_playlist_item_ids_from_names(youtube: Any, playlist_names: list[str]) -> set[str]:
    playlist_ids = get_playlist_ids_from_names(youtube, playlist_names)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    return {item["id"] for item in items}


def read_video_ids_from_files(file_paths: list[str]) -> set[str]:
    video_ids = set()
    for file_path in file_paths:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    video_ids.add(line)
    return video_ids


def get_video_ids_from_playlist_names(youtube: Any, names: list[str]) -> set[str]:
    playlist_ids = get_playlist_ids_from_names(youtube, names)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    return {item["snippet"]["resourceId"]["videoId"] for item in items}


def get_items_from_playlist_names(youtube: Any, names: list[str]) -> list[dict[str, Any]]:
    playlist_ids = get_playlist_ids_from_names(youtube, names)
    return get_all_items_from_playlist_ids(youtube, playlist_ids)


METADATA_FIELDNAMES = [
    "video_id", "title", "description", "duration", "upload_date",
    "uploader", "uploader_id", "channel", "channel_id",
    "view_count", "like_count", "comment_count", "average_rating",
    "age_limit", "categories", "tags", "is_live", "was_live", "live_status",
    "resolution", "fps", "vcodec", "acodec", "width", "height",
    "thumbnail", "webpage_url", "availability", "playable_in_embed",
    "channel_follower_count", "language", "subtitles_available",
    "automatic_captions_available",
]


def add_video_to_playlist(youtube: Any, playlist_id: str, video_id: str) -> None:
    logger = logging.getLogger()
    logger.info(f"adding video [{video_id}] to playlist [{playlist_id}]")
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            },
        },
    )
    retry_execute(request)


def get_playlist_item_count(youtube: Any, playlist_id: str) -> int:
    items = get_all_items_from_playlist_id(youtube, playlist_id)
    return len(items)


def get_video_metadata(video_id: str) -> dict[str, Any] | None:
    logger = logging.getLogger()
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignore_no_formats_error": True,
    }
    try:
        logger.info(f"Fetching data for ID: {video_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
        if not info_dict:
            return None
        metadata: dict[str, Any] = {
            "video_id": video_id,
            "title": info_dict.get("title", ""),
            "description": info_dict.get("description", ""),
            "duration": info_dict.get("duration", ""),
            "upload_date": info_dict.get("upload_date", ""),
            "uploader": info_dict.get("uploader", ""),
            "uploader_id": info_dict.get("uploader_id", ""),
            "channel": info_dict.get("channel", ""),
            "channel_id": info_dict.get("channel_id", ""),
            "view_count": info_dict.get("view_count", ""),
            "like_count": info_dict.get("like_count", ""),
            "comment_count": info_dict.get("comment_count", ""),
            "average_rating": info_dict.get("average_rating", ""),
            "age_limit": info_dict.get("age_limit", ""),
            "categories": ", ".join(info_dict.get("categories", [])) if info_dict.get("categories") else "",
            "tags": ", ".join(info_dict.get("tags", [])) if info_dict.get("tags") else "",
            "is_live": info_dict.get("is_live", ""),
            "was_live": info_dict.get("was_live", ""),
            "live_status": info_dict.get("live_status", ""),
            "resolution": info_dict.get("resolution", ""),
            "fps": info_dict.get("fps", ""),
            "vcodec": info_dict.get("vcodec", ""),
            "acodec": info_dict.get("acodec", ""),
            "width": info_dict.get("width", ""),
            "height": info_dict.get("height", ""),
            "thumbnail": info_dict.get("thumbnail", ""),
            "webpage_url": info_dict.get("webpage_url", ""),
            "availability": info_dict.get("availability", ""),
            "playable_in_embed": info_dict.get("playable_in_embed", ""),
            "channel_follower_count": info_dict.get("channel_follower_count", ""),
            "language": info_dict.get("language", ""),
            "subtitles_available":
                ", ".join(info_dict.get("subtitles", {}).keys()) if info_dict.get("subtitles") else "",
            "automatic_captions_available":
                ", ".join(info_dict.get("automatic_captions", {}).keys()) if info_dict.get("automatic_captions") else "",
        }
        return metadata
    except Exception as e:  # noqa: BLE001  # pylint: disable=broad-exception-caught
        logger.warning(f"An unexpected error occurred for ID {video_id}: {e}")
        return None
