"""
main entry point to the program
"""
import logging

import googleapiclient.discovery
import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit import LOGGER_NAME
from pytubekit.auth import get_credentials
from pytubekit.version import VERSION_STR

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]
APP_NAME = "pytubekit"


@register_endpoint()
def version() -> None:
    """
    Print version
    """
    print(VERSION_STR)


@register_endpoint()
def playlists() -> None:
    """
    Show all playlists in your youtube account
    """
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


@register_endpoint()
def cleanup() -> None:
    """
    Cleanup a specific playlist from deleted or privatized entries
    """
    print("TBD")


@register_main()
def main():
    """
    Pytubekit will allow you to perform operations in your youtube account en masse
    """
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
