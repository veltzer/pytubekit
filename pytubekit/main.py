"""
main entry point to the program
"""
import logging
import os

import googleapiclient.discovery
import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit import LOGGER_NAME
from pytubekit.auth import get_credentials
from pytubekit.static import DESCRIPTION, APP_NAME, VERSION_STR


# all of the following you get from the YouTube API documentation
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]


@register_endpoint(
    description="Show all playlists in your youtube account",
)
def playlists() -> None:
    logger = logging.getLogger(LOGGER_NAME)
    credentials = get_credentials(
        logger=logger,
        scopes=SCOPES,
        app_name=APP_NAME,
    )
    youtube = googleapiclient.discovery.build(
        serviceName=API_SERVICE_NAME,
        version=API_VERSION,
        credentials=credentials,
        cache_discovery=False,
    )
    # pylint: disable=no-member
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True,
    )
    response = request.execute()
    for x in response["items"]:
        print(x["snippet"]["title"])


@register_endpoint(
    description="Cleanup a specific playlist from deleted or privatized entries",
)
def cleanup() -> None:
    print("TBD")


@register_endpoint(
    description="collect you tube video ids from files",
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
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
