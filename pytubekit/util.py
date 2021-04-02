import logging

import googleapiclient.discovery
from pygooglehelper import get_credentials, ConfigAuth

from pytubekit import LOGGER_NAME
from pytubekit.configs import ConfigPagination
from pytubekit.scopes import SCOPES
from pytubekit.static import APP_NAME

# all of the following you get from the YouTube API documentation
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

NEXT_PAGE_TOKEN = "nextPageToken"
PAGE_TOKEN = "pageToken"
ITEMS_TOKEN = "items"


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


def create_playlists(youtube) -> PagedRequest:
    kwargs = {
        "part": "snippet",
        "maxResults": ConfigPagination.page_size,
        "mine": True,
    }
    return PagedRequest(f=youtube.playlists().list, kwargs=kwargs)


def create_playlist(youtube, playlist_id: str) -> PagedRequest:
    kwargs = {
        "part": "snippet,id",
        "playlistId": playlist_id,
        "maxResults": ConfigPagination.page_size,
    }
    return PagedRequest(f=youtube.playlistItems().list, kwargs=kwargs)


def get_playlist_id_from_name(youtube, playlist_name: str) -> str:
    d = {}
    r = create_playlists(youtube)
    items = r.get_all_items()
    for item in items:
        f_id = item["id"]
        f_title = item["snippet"]["title"]
        d[f_title] = f_id
    return d[playlist_name]


def get_youtube():
    logger = logging.getLogger(LOGGER_NAME)
    credentials = get_credentials(
        logger=logger,
        scopes=SCOPES,
        app_name=APP_NAME,
        host=ConfigAuth.host,
        port=ConfigAuth.port,
        authorization_prompt_message=ConfigAuth.authorization_prompt_message,
    )
    youtube = googleapiclient.discovery.build(
        serviceName=API_SERVICE_NAME,
        version=API_VERSION,
        credentials=credentials,
        cache_discovery=False,
    )
    return youtube
