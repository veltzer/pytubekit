import json
import logging
import sys
from typing import List, Set

import googleapiclient.discovery
from pygooglehelper import get_credentials, ConfigRequest

from pytubekit.configs import ConfigPagination, ConfigPlaylist
from pytubekit.constants import SCOPES, API_SERVICE_NAME, API_VERSION, NEXT_PAGE_TOKEN, PAGE_TOKEN, ITEMS_TOKEN
from pytubekit.static import APP_NAME


class PagedRequest:
    def __init__(self, f, kwargs):
        self.f = f
        self.next_page_token = None
        self.kwargs = kwargs

    def get_next_page(self):
        if self.next_page_token is not None:
            self.kwargs[PAGE_TOKEN] = self.next_page_token
        request = self.f(**self.kwargs)
        response = request.execute()
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


def get_playlist_ids_from_names(youtube, playlist_names: List[str]) -> List[str]:
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    name_to_id = {item["snippet"]["title"]: item["id"] for item in items}
    return [name_to_id[playlist_name] for playlist_name in playlist_names]


def get_all_items(youtube):
    playlist_id = get_playlist_ids_from_names(youtube, [ConfigPlaylist.name])[0]
    return get_all_items_from_playlist_id(youtube, playlist_id)


def get_all_items_from_playlist_id(youtube, playlist_id: str):
    return create_playlist_request(youtube, playlist_id=playlist_id).get_all_items()


def get_all_items_from_playlist_ids(youtube, playlist_ids: List[str]):
    items = []
    for playlist_id in playlist_ids:
        items.extend(get_all_items_from_playlist_id(youtube, playlist_id))
    return items


def delete_playlist_item_by_id(youtube, playlist_item_id: str):
    logger = logging.getLogger()
    logger.info(f"deleting playlist item {playlist_item_id}")
    request = youtube.playlistItems().delete(
        id=playlist_item_id,
    )
    request.execute()


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
    return request.execute()


def pretty_print(data, fp=sys.stdout):
    json.dump(data, fp, indent=4)


def get_youtube_channels(youtube):
    return youtube.channels()


def get_youtube_playlists(youtube):
    return youtube.playlists()


def get_my_playlists_ids(youtube) -> List[str]:
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    ids = []
    for item in items:
        ids.append(item["id"])
    return ids


def get_playlist_item_ids_from_names(youtube, playlist_names) -> Set[str]:
    playlist_ids = get_playlist_ids_from_names(youtube, playlist_names)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    return {item["id"] for item in items}
