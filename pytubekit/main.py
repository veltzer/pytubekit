"""
main entry point to the program
"""
import logging
import os

import pylogconf.core
# import pyvardump
from pygooglehelper import register_functions
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit.configs import ConfigPlaylist, ConfigPagination, ConfigDelete
from pytubekit.scopes import SCOPES
from pytubekit.static import DESCRIPTION, APP_NAME, VERSION_STR
from pytubekit.util import create_playlists, get_youtube, create_playlist, get_all_items, delete_playlist_item_by_id


@register_endpoint(
    description="Show all playlists in your youtube account",
    configs=[ConfigPagination],
)
def playlists() -> None:
    youtube = get_youtube()
    r = create_playlists(youtube)
    items = r.get_all_items()
    for item in items:
        f_title = item["snippet"]["title"]
        print(f"{f_title}")


@register_endpoint(
    description="List all entries in a playlist",
    configs=[ConfigPagination, ConfigPlaylist],
)
def playlist() -> None:
    youtube = get_youtube()
    items = get_all_items(youtube)
    for item in items:
        f_video_id = item["snippet"]["resourceId"]["videoId"]
        print(f"{f_video_id}")


@register_endpoint(
    description="Dump all playlists",
    configs=[ConfigPagination],
)
def dump() -> None:
    youtube = get_youtube()
    r = create_playlists(youtube)
    items = r.get_all_items()
    id_to_title = {}
    for item in items:
        f_id = item["id"]
        f_title = item["snippet"]["title"]
        id_to_title[f_id] = f_title
    print("got lists data")
    for f_id, f_title in id_to_title.items():
        print(f"dumping [{f_title}]")
        with open(f_title, "w") as f:
            r = create_playlist(youtube, playlist_id=f_id)
            items = r.get_all_items()
            for item in items:
                f_video_id = item["snippet"]["resourceId"]["videoId"]
                print(f"{f_video_id}", file=f)


@register_endpoint(
    description="Remove duplicates from a playlist",
    configs=[ConfigPagination, ConfigPlaylist],
)
def dedup() -> None:
    youtube = get_youtube()
    items = get_all_items(youtube)
    seen = set()
    wanted_to_delete = 0
    deleted = 0
    for item in items:
        f_video_id = item["snippet"]["resourceId"]["videoId"]
        if f_video_id in seen:
            wanted_to_delete += 1
            if ConfigDelete.doit:
                f_id = item["id"]
                delete_playlist_item_by_id(youtube, f_id)
                deleted += 1
        else:
            seen.add(f_video_id)
    logger = logging.getLogger()
    logger.info(f"wanted_to_delete {wanted_to_delete} items")
    logger.info(f"deleted {deleted} items")


@register_endpoint(
    description="Mark all entries in playlist as seen",
    configs=[ConfigPagination, ConfigPlaylist],
)
def mark_seen() -> None:
    print("TBD")


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
