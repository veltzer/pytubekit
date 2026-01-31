"""
util.py
"""

import json
import logging
import subprocess
import sys
import time

import googleapiclient.discovery
from googleapiclient.errors import HttpError
from pygooglehelper import get_credentials, ConfigRequest

from pytubekit.configs import ConfigPagination, ConfigPlaylist
from pytubekit.constants import SCOPES, API_SERVICE_NAME, API_VERSION, NEXT_PAGE_TOKEN, PAGE_TOKEN, ITEMS_TOKEN
from pytubekit.static import APP_NAME


def log_progress(logger, current: int, total: int, interval: int = 100):
    if current % interval == 0 or current == total:
        logger.info(f"progress: {current}/{total}")


def retry_execute(request, max_retries: int = 5):
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
    def __init__(self, f, kwargs):
        self.f = f
        self.next_page_token = None
        self.kwargs = kwargs

    def get_next_page(self):
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

    def get_all_items(self):
        items = []
        while True:
            over, response = self.get_next_page()
            # print(f"got {len(response[ITEMS_TOKEN])} items")
            items.extend(response[ITEMS_TOKEN])
            if over:
                break
        return items


def create_playlists_request(youtube) -> PagedRequest:
    kwargs = {
        "part": "snippet",
        "maxResults": ConfigPagination.page_size,
        "mine": True,
    }
    return PagedRequest(f=youtube.playlists().list, kwargs=kwargs)


def create_playlist_request(youtube, playlist_id: str) -> PagedRequest:
    kwargs = {
        "part": "snippet,id",
        "playlistId": playlist_id,
        "maxResults": ConfigPagination.page_size,
    }
    return PagedRequest(f=youtube.playlistItems().list, kwargs=kwargs)


def get_playlist_ids_from_names(youtube, playlist_names: list[str]) -> list[str]:
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    name_to_id = {item["snippet"]["title"]: item["id"] for item in items}
    return [name_to_id[playlist_name] for playlist_name in playlist_names]


def get_all_items(youtube):
    if ConfigPlaylist.name is not None:
        playlist_id = get_playlist_ids_from_names(youtube, [ConfigPlaylist.name])[0]
    else:
        playlist_id = ConfigPlaylist.playlist_id
    return get_all_items_from_playlist_id(youtube, playlist_id)


def get_all_items_from_playlist_id(youtube, playlist_id: str):
    return create_playlist_request(youtube, playlist_id=playlist_id).get_all_items()


def get_all_items_from_playlist_ids(youtube, playlist_ids: list[str]):
    items = []
    for playlist_id in playlist_ids:
        items.extend(get_all_items_from_playlist_id(youtube, playlist_id))
    return items


def delete_playlist_item_by_id(youtube, playlist_item_id: str):
    logger = logging.getLogger()
    logger.info(f"deleting playlist item [{playlist_item_id}]")
    request = youtube.playlistItems().delete(
        id=playlist_item_id,
    )
    retry_execute(request)


def get_youtube():
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


def get_video_info(youtube, youtube_id):
    request = youtube.videos().list(
        part="snippet,status,snippet,contentDetails",
        id=youtube_id,
    )
    return retry_execute(request)


def pretty_print(data, fp=sys.stdout):
    json.dump(data, fp, indent=4)


def get_youtube_channels(youtube):
    return youtube.channels()


def get_youtube_playlists(youtube):
    return youtube.playlists()


def get_my_playlists_ids(youtube) -> list[str]:
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    ids = []
    for item in items:
        ids.append(item["id"])
    return ids


def get_playlist_item_ids_from_names(youtube, playlist_names) -> set[str]:
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


def get_video_ids_from_playlist_names(youtube, names: list[str]) -> set[str]:
    playlist_ids = get_playlist_ids_from_names(youtube, names)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    return {item["snippet"]["resourceId"]["videoId"] for item in items}


def get_items_from_playlist_names(youtube, names: list[str]):
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


def add_video_to_playlist(youtube, playlist_id: str, video_id: str):
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


def get_playlist_item_count(youtube, playlist_id: str) -> int:
    items = get_all_items_from_playlist_id(youtube, playlist_id)
    return len(items)


def get_video_metadata(video_id: str) -> dict | None:
    logger = logging.getLogger()
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        logger.info(f"Fetching data for ID: {video_id}...")
        cmd = [
            "yt-dlp",
            "-j",
            "--no-warnings",
            "--skip-download",
            video_url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode != 0 and "format" in result.stderr.lower():
            cmd_fallback = [
                "yt-dlp",
                "-j",
                "--no-warnings",
                "--skip-download",
                "--ignore-no-formats-error",
                video_url,
            ]
            result = subprocess.run(cmd_fallback, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode != 0:
            logger.warning(f"Error fetching ID {video_id}: {result.stderr}")
            return None
        if not result.stdout:
            return None
        info_dict = json.loads(result.stdout)
        if not info_dict:
            return None
        metadata = {
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
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout fetching ID {video_id}")
        return None
    except json.JSONDecodeError as e:
        logger.warning(f"Error parsing JSON for ID {video_id}: {e}")
        return None
    except Exception as e:  # noqa: BLE001  # pylint: disable=broad-exception-caught
        logger.warning(f"An unexpected error occurred for ID {video_id}: {e}")
        return None
