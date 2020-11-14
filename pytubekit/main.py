"""
main entry point to the program
"""
import logging
import os

import googleapiclient.discovery
import pylogconf.core
import pyvardump
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit import LOGGER_NAME
from pytubekit.auth import get_credentials
from pytubekit.configs import ConfigAuth, ConfigPlaylist
from pytubekit.static import DESCRIPTION, APP_NAME, VERSION_STR


# all of the following you get from the YouTube API documentation
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]


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


@register_endpoint(
    description="Show all playlists in your youtube account",
)
def playlists() -> None:
    youtube = get_youtube()
    # pylint: disable=no-member
    request = youtube.playlists().list(
        # part="snippet,contentDetails",
        # part="contentDetails",
        part="status",
        maxResults=5,
        mine=True,
    )
    response = request.execute()
    pyvardump.dump_pprint(response)
    import sys
    sys.exit(1)

    for x in response["items"]:
        pyvardump.dump_pprint(x["snippet"])
        import sys
        sys.exit(1)
        print(x["snippet"]["title"])
        print(x["snippet"]["description"])


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


@register_endpoint(
    description="Do the authentication procedure and get token for your app",
    configs=[ConfigAuth],
)
def auth() -> None:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    get_credentials(
        logger=logger,
        scopes=SCOPES,
        app_name=APP_NAME,
        host=ConfigAuth.host,
        port=ConfigAuth.port,
        authorization_prompt_message=ConfigAuth.authorization_prompt_message,
        force=ConfigAuth.force,
    )


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
