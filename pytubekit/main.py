"""
main entry point to the program
"""
import json
import logging
import os
import sys

import pylogconf.core
# import pyvardump
from pygooglehelper import register_functions
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit.configs import ConfigPlaylist, ConfigPagination, ConfigCleanup, ConfigPlaylists, ConfigVideo, ConfigPrint
from pytubekit.constants import SCOPES, DELETED_TITLE
from pytubekit.static import DESCRIPTION, APP_NAME, VERSION_STR
from pytubekit.util import create_playlists, get_youtube, create_playlist, get_all_items, delete_playlist_item_by_id, \
    get_playlist_ids_from_names, get_all_items_from_playlist_ids, get_video_info


@register_endpoint(
    description="Show all playlists in your youtube account",
    configs=[ConfigPagination],
)
def playlists() -> None:
    youtube = get_youtube()
    r = create_playlists(youtube)
    items = r.get_all_items()
    for item in items:
        if ConfigPrint.full:
            json.dump(item, indent=4, fp=sys.stdout)
        else:
            f_title = item["snippet"]["title"]
            print(f"{f_title}")


@register_endpoint(
    description="List all entries in a playlist",
    configs=[ConfigPagination, ConfigPlaylist, ConfigPrint],
)
def playlist() -> None:
    youtube = get_youtube()
    items = get_all_items(youtube)
    for item in items:
        if ConfigPrint.full:
            json.dump(item, indent=4, fp=sys.stdout)
        else:
            f_video_id = item["snippet"]["resourceId"]["videoId"]
            print(f"{f_video_id}")


@register_endpoint(
    description="Dump all playlists",
    configs=[ConfigPagination, ConfigPrint],
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
                if ConfigPrint.full:
                    json.dump(item, indent=4, fp=f)
                else:
                    print(f"{f_video_id}", file=f)


@register_endpoint(
    description="Clean up a set of playlists (dedup, remove deleted, remove privatized)",
    configs=[ConfigPagination, ConfigPlaylists, ConfigCleanup],
)
def cleanup() -> None:
    youtube = get_youtube()
    playlist_ids = get_playlist_ids_from_names(youtube, ConfigPlaylists.names)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    seen = set()
    wanted_to_delete = 0
    deleted = 0
    saw = 0
    found_duplicates = 0
    found_deleted = 0
    for item in items:
        to_delete = False
        saw += 1
        if ConfigCleanup.dedup:
            f_video_id = item["snippet"]["resourceId"]["videoId"]
            if f_video_id in seen:
                found_duplicates += 1
                to_delete = True
            else:
                seen.add(f_video_id)
        if ConfigCleanup.deleted:
            f_title = item["snippet"]["title"]
            if f_title == DELETED_TITLE:
                found_deleted += 1
                to_delete = True
        if to_delete:
            wanted_to_delete += 1
            if ConfigCleanup.do_delete:
                f_id = item["id"]
                delete_playlist_item_by_id(youtube, f_id)
                deleted += 1
    logger = logging.getLogger()
    logger.info(f"saw {saw} items")
    logger.info(f"found_duplicates {found_duplicates} items")
    logger.info(f"found_deleted {found_deleted} items")
    logger.info(f"wanted_to_delete {wanted_to_delete} items")
    logger.info(f"deleted {deleted} items")


@register_endpoint(
    description="get info about a video",
    configs=[ConfigVideo],
)
def video_info() -> None:
    youtube = get_youtube()
    info = get_video_info(youtube, ConfigVideo.id)
    json.dump(info, fp=sys.stdout, indent=4)


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
