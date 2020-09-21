"""
The default group of operations that pytubekit has
"""
import logging

from pytconf import register_endpoint, register_function_group


import googleapiclient.discovery
import googleapiclient.errors


import pytubekit
import pytubekit.version
from pytubekit.auth import get_credentials


API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pytubekit commands"

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]
APP_NAME = "pytubekit"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(group=GROUP_NAME_DEFAULT, )
def version() -> None:
    """
    Print version
    """
    print(pytubekit.version.VERSION_STR)


@register_endpoint(group=GROUP_NAME_DEFAULT, )
def playlists() -> None:
    """
    Show all playlists in your youtube account
    """
    logger = logging.getLogger(pytubekit.LOGGER_NAME)
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


@register_endpoint(group=GROUP_NAME_DEFAULT, )
def cleanup() -> None:
    """
    Cleanup a specific playlist from deleted or privatized entries
    """
    print("TBD")
