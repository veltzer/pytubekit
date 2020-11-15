"""
main entry point to the program
"""
import logging
import os

import googleapiclient.discovery
import pylogconf.core
# import pyvardump
from pygooglehelper import register_functions, get_credentials, ConfigAuth
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit import LOGGER_NAME
from pytubekit.configs import ConfigPlaylist
from pytubekit.static import DESCRIPTION, APP_NAME, VERSION_STR


# all of the following you get from the YouTube API documentation
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]
NEXT_PAGE_TOKEN = "nextPageToken"
PAGE_TOKEN = "pageToken"


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


def create_list_request(youtube, next_page_token):
    kwargs = {
        # part="snippet,contentDetails",
        # part="contentDetails",
        # part="status",
        "part": "snippet",
        "maxResults": 25,
        "mine": True,
    }
    if next_page_token:
        kwargs[PAGE_TOKEN] = next_page_token
    return youtube.playlists().list(**kwargs)


@register_endpoint(
    description="Show all playlists in your youtube account",
)
def playlists() -> None:
    youtube = get_youtube()

    next_page_token = None
    while True:
        request = create_list_request(youtube, next_page_token)
        response = request.execute()
        # pyvardump.dump_pprint(response)
        # import sys
        # sys.exit(1)

        for x in response["items"]:
            # pyvardump.dump_pprint(x["snippet"])
            # import sys
            # sys.exit(1)
            print(x["snippet"]["title"])
            # print(x["snippet"]["description"])
        if NEXT_PAGE_TOKEN in response:
            next_page_token = response[NEXT_PAGE_TOKEN]
        else:
            break


@register_endpoint(
    description="Mark all entries in playlist as seen",
    configs=[ConfigPlaylist],
)
def mark_seen() -> None:
    # youtube = get_youtube()
    pass


@register_endpoint(
    description="Cleanup a specific playlist from deleted or privatized entries",
)
def cleanup() -> None:
    print("TBD")


@register_endpoint(
    description="Collect you tube video ids from files",
)
def collect_ids() -> None:
    for filename in os.listdir():
        _, extension = os.path.splitext(filename)
        print(extension)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    register_functions(scopes=SCOPES, app_name=APP_NAME)
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
