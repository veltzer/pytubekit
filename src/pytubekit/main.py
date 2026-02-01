"""
main entry point to the program
"""
import csv
import logging
import os
import pathlib
import re
import string
import time

import pylogconf.core
from pygooglehelper import register_functions, ConfigRequest
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pytubekit.configs import ConfigPlaylist, ConfigPagination, ConfigCleanup, ConfigVideo, \
    ConfigPrint, ConfigDump, ConfigSubtract, ConfigDelete, ConfigDiff, ConfigAddData, ConfigOverflow, \
    ConfigCleanupPlaylists, ConfigCount, ConfigClear, ConfigCopy, ConfigMerge, ConfigSort, ConfigSearch, \
    ConfigExportCsv, ConfigRename, ConfigLeftToSee, ConfigCollectIds, ConfigAddFileToPlaylist
from pytubekit.constants import SCOPES, MAX_PLAYLIST_ITEMS
from pytubekit.static import DESCRIPTION, APP_NAME, VERSION_STR
from pytubekit.util import create_playlists_request, get_youtube, create_playlist_request, get_all_items, \
    delete_playlist_item_by_id, get_playlist_ids_from_names, get_all_items_from_playlist_ids, \
    get_video_info, pretty_print, get_youtube_channels, get_youtube_playlists, get_my_playlists_ids, \
    read_video_ids_from_files, get_video_ids_from_playlist_names, \
    get_items_from_playlist_names, get_video_metadata, METADATA_FIELDNAMES, \
    add_video_to_playlist, get_playlist_item_count, log_progress, retry_execute, cleanup_items
from pytubekit.youtube import youtube_dl_download_urls


@register_endpoint(
    description="Show me my channel id",
    configs=[],
)
def get_channel_id() -> None:
    youtube = get_youtube()
    channels_obj = get_youtube_channels(youtube)
    request = channels_obj.list(
        part="id",
        mine=True
    )
    response = retry_execute(request)
    print(response["items"][0]["id"])


@register_endpoint(
    description="Show me my channel id",
    configs=[],
)
def get_watch_later_playlist_id() -> None:
    youtube = get_youtube()
    channels_obj = get_youtube_channels(youtube)
    request = channels_obj.list(
        part="id",
        mine=True
    )
    response = retry_execute(request)
    channel_id = response["items"][0]["id"]
    playlist_id = channel_id[0] + "L" + channel_id[2:]
    print(playlist_id)


@register_endpoint(
    description="Show all playlists in your youtube account",
    configs=[ConfigPagination],
)
def playlists() -> None:
    youtube = get_youtube()
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    for item in items:
        if ConfigPrint.full:
            pretty_print(item)
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
            pretty_print(item)
        else:
            f_video_id = item["snippet"]["resourceId"]["videoId"]
            print(f"{f_video_id}")


@register_endpoint(
    description="Dump all playlists",
    configs=[ConfigPagination, ConfigPrint, ConfigDump],
)
def dump() -> None:
    logger = logging.getLogger()
    sub_dict = {
        "date": int(time.time()),
        "home": os.path.expanduser("~"),
    }
    dump_folder = string.Template(ConfigDump.dump_folder).substitute(sub_dict)
    pathlib.Path(dump_folder).mkdir(parents=True, exist_ok=True)

    youtube = get_youtube()
    r = create_playlists_request(youtube)
    items = r.get_all_items()
    id_to_title = {}
    for item in items:
        f_id = item["id"]
        f_title = item["snippet"]["title"]
        id_to_title[f_id] = f_title
    logger.info("got lists data")
    for f_id, f_title in id_to_title.items():
        filename = os.path.join(dump_folder, f_title)
        logger.info(f"dumping [{f_title}] to [{filename}]")
        with open(filename, "w") as f:
            r = create_playlist_request(youtube, playlist_id=f_id)
            items = r.get_all_items()
            for item in items:
                f_video_id = item["snippet"]["resourceId"]["videoId"]
                if ConfigPrint.full:
                    pretty_print(item, fp=f)
                else:
                    print(f"{f_video_id}", file=f)


@register_endpoint(
    description="Clean up a set of playlists (dedup, remove deleted, remove privatized)",
    configs=[ConfigPagination, ConfigCleanupPlaylists, ConfigCleanup, ConfigDelete],
)
def cleanup() -> None:
    logger = logging.getLogger()
    logger.info(f"cleaning up [{ConfigCleanupPlaylists.cleanup_names}]...")
    youtube = get_youtube()
    playlist_ids = get_playlist_ids_from_names(youtube, ConfigCleanupPlaylists.cleanup_names)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    cleanup_items(
        youtube, items,
        dedup=ConfigCleanup.dedup,
        check_deleted=ConfigCleanup.deleted,
        check_privatized=ConfigCleanup.privatized,
        do_delete=ConfigDelete.do_delete,
    )


@register_endpoint(
    description="Remove unavialable or privatized from all playlists",
    configs=[ConfigPagination, ConfigCleanup, ConfigDelete],
)
def remove_unavailable_from_all_playlists() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    playlists_ids = get_my_playlists_ids(youtube)
    logger.info(f"working on playlist ids[{playlists_ids}]...")
    items = get_all_items_from_playlist_ids(youtube, playlists_ids)
    cleanup_items(
        youtube, items,
        dedup=False,
        check_deleted=ConfigCleanup.deleted,
        check_privatized=ConfigCleanup.privatized,
        do_delete=ConfigDelete.do_delete,
    )


@register_endpoint(
    description="Remove videos from A playlists that exist in B playlists (A = A - B)",
    configs=[ConfigPagination, ConfigSubtract, ConfigDelete],
)
def subtract() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    logger.info(f"subtracting [{ConfigSubtract.subtract_what}] from [{ConfigSubtract.subtract_from}]...")
    what_video_ids = get_video_ids_from_playlist_names(youtube, ConfigSubtract.subtract_what)
    from_items = get_items_from_playlist_names(youtube, ConfigSubtract.subtract_from)
    deleted = 0
    wanted_to_delete = 0
    total = len(from_items)
    for i, item in enumerate(from_items, start=1):
        log_progress(logger, i, total)
        video_id = item["snippet"]["resourceId"]["videoId"]
        if video_id in what_video_ids:
            wanted_to_delete += 1
            if ConfigDelete.do_delete:
                delete_playlist_item_by_id(youtube, item["id"])
                deleted += 1
    logger.info(f"wanted_to_delete {wanted_to_delete} items")
    logger.info(f"deleted {deleted} items")


@register_endpoint(
    description="Delete all items from a playlist",
    configs=[ConfigPagination, ConfigClear, ConfigDelete],
)
def clear_playlist() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    playlist_id = get_playlist_ids_from_names(youtube, [ConfigClear.clear_name])[0]
    items = get_all_items_from_playlist_ids(youtube, [playlist_id])
    logger.info(f"playlist [{ConfigClear.clear_name}] has {len(items)} items")
    deleted = 0
    total = len(items)
    for i, item in enumerate(items, start=1):
        log_progress(logger, i, total)
        if ConfigDelete.do_delete:
            delete_playlist_item_by_id(youtube, item["id"])
            deleted += 1
    logger.info(f"deleted {deleted} items from [{ConfigClear.clear_name}]")


@register_endpoint(
    description="Print the item count for one or more playlists",
    configs=[ConfigPagination, ConfigCount],
)
def count() -> None:
    youtube = get_youtube()
    playlist_ids = get_playlist_ids_from_names(youtube, ConfigCount.count_names)
    for playlist_name, playlist_id in zip(ConfigCount.count_names, playlist_ids):
        item_count = get_playlist_item_count(youtube, playlist_id)
        print(f"{playlist_name}: {item_count}")


@register_endpoint(
    description="Copy all videos from one playlist to another",
    configs=[ConfigPagination, ConfigCopy],
)
def copy_playlist() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    source_id, destination_id = get_playlist_ids_from_names(
        youtube, [ConfigCopy.copy_source, ConfigCopy.copy_destination],
    )
    items = get_all_items_from_playlist_ids(youtube, [source_id])
    logger.info(f"source [{ConfigCopy.copy_source}] has {len(items)} items")
    copied = 0
    total = len(items)
    for item in items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        add_video_to_playlist(youtube, destination_id, video_id)
        copied += 1
        log_progress(logger, copied, total)
    logger.info(f"copied {copied} videos from [{ConfigCopy.copy_source}] to [{ConfigCopy.copy_destination}]")


@register_endpoint(
    description="Merge several playlists into one destination playlist, deduplicating",
    configs=[ConfigPagination, ConfigMerge],
)
def merge() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    all_names = ConfigMerge.merge_sources + [ConfigMerge.merge_destination]
    all_ids = get_playlist_ids_from_names(youtube, all_names)
    source_ids = all_ids[:-1]
    destination_id = all_ids[-1]
    dest_items = get_all_items_from_playlist_ids(youtube, [destination_id])
    seen = {item["snippet"]["resourceId"]["videoId"] for item in dest_items}
    logger.info(f"destination [{ConfigMerge.merge_destination}] already has {len(seen)} videos")
    source_items = get_all_items_from_playlist_ids(youtube, source_ids)
    logger.info(f"source playlists have {len(source_items)} items total")
    added = 0
    skipped = 0
    total = len(source_items)
    for i, item in enumerate(source_items, start=1):
        log_progress(logger, i, total)
        video_id = item["snippet"]["resourceId"]["videoId"]
        if video_id in seen:
            skipped += 1
            continue
        add_video_to_playlist(youtube, destination_id, video_id)
        seen.add(video_id)
        added += 1
    logger.info(f"added {added} videos, skipped {skipped} duplicates")


SORT_KEYS = {
    "title": lambda item: item["snippet"].get("title", "").lower(),
    "channel": lambda item: item["snippet"].get("videoOwnerChannelTitle", "").lower(),
    "date": lambda item: item["snippet"].get("publishedAt", ""),
}


@register_endpoint(
    description="Sort a playlist by title, channel, or date (deletes and re-adds all items)",
    configs=[ConfigPagination, ConfigSort],
)
def sort_playlist() -> None:
    logger = logging.getLogger()
    if ConfigSort.sort_key not in SORT_KEYS:
        logger.error(f"invalid sort key [{ConfigSort.sort_key}], must be one of {list(SORT_KEYS.keys())}")
        return
    youtube = get_youtube()
    playlist_id = get_playlist_ids_from_names(youtube, [ConfigSort.sort_playlist_name])[0]
    items = get_all_items_from_playlist_ids(youtube, [playlist_id])
    logger.info(f"playlist [{ConfigSort.sort_playlist_name}] has {len(items)} items")
    sorted_items = sorted(items, key=SORT_KEYS[ConfigSort.sort_key])
    total = len(items)
    for i, item in enumerate(items, start=1):
        delete_playlist_item_by_id(youtube, item["id"])
        log_progress(logger, i, total)
    logger.info(f"deleted {total} items")
    added = 0
    for item in sorted_items:
        video_id = item["snippet"]["resourceId"]["videoId"]
        add_video_to_playlist(youtube, playlist_id, video_id)
        added += 1
        log_progress(logger, added, total)
    logger.info(f"re-added {added} items in sorted order (by {ConfigSort.sort_key})")


@register_endpoint(
    description="Search for videos by title or channel name across one or more playlists",
    configs=[ConfigPagination, ConfigSearch],
)
def search_playlist() -> None:
    youtube = get_youtube()
    playlist_ids = get_playlist_ids_from_names(youtube, ConfigSearch.search_playlists)
    items = get_all_items_from_playlist_ids(youtube, playlist_ids)
    query = str(ConfigSearch.search_query).lower()
    for item in items:
        title = item["snippet"].get("title", "")
        channel = item["snippet"].get("videoOwnerChannelTitle", "")
        if query in title.lower() or query in channel.lower():
            video_id = item["snippet"]["resourceId"]["videoId"]
            print(f"{video_id}  {title}  [{channel}]")


@register_endpoint(
    description="Export a playlist to CSV with video ID, title, channel, and position",
    configs=[ConfigPagination, ConfigExportCsv],
)
def export_csv() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    playlist_id = get_playlist_ids_from_names(youtube, [ConfigExportCsv.export_playlist_name])[0]
    items = get_all_items_from_playlist_ids(youtube, [playlist_id])
    fieldnames = ["position", "video_id", "title", "channel"]
    with open(str(ConfigExportCsv.export_csv_path), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for position, item in enumerate(items, start=1):
            writer.writerow({
                "position": position,
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"].get("title", ""),
                "channel": item["snippet"].get("videoOwnerChannelTitle", ""),
            })
    logger.info(f"exported {len(items)} items to [{ConfigExportCsv.export_csv_path}]")


@register_endpoint(
    description="Rename a playlist",
    configs=[ConfigRename],
)
def rename_playlist() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    playlist_id = get_playlist_ids_from_names(youtube, [ConfigRename.rename_playlist_name])[0]
    request = youtube.playlists().update(
        part="snippet",
        body={
            "id": playlist_id,
            "snippet": {
                "title": str(ConfigRename.rename_new_name),
            },
        },
    )
    retry_execute(request)
    logger.info(f"renamed [{ConfigRename.rename_playlist_name}] to [{ConfigRename.rename_new_name}]")


@register_endpoint(
    description="List unseen videos by subtracting seen playlists from source playlists",
    configs=[ConfigPagination, ConfigLeftToSee],
)
def left_to_see() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    all_video_ids = get_video_ids_from_playlist_names(youtube, ConfigLeftToSee.lts_all_playlists)
    seen_video_ids = get_video_ids_from_playlist_names(youtube, ConfigLeftToSee.lts_seen_playlists)
    unseen = sorted(all_video_ids - seen_video_ids)
    logger.info(f"total {len(all_video_ids)}, seen {len(seen_video_ids)}, unseen {len(unseen)}")
    for video_id in unseen:
        print(video_id)


@register_endpoint(
    description="Move videos from source playlist to destination playlist respecting the 5000 limit",
    configs=[ConfigPagination, ConfigOverflow, ConfigDelete],
)
def overflow() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    source_id, destination_id = get_playlist_ids_from_names(
        youtube, [ConfigOverflow.source, ConfigOverflow.destination],
    )
    destination_count = get_playlist_item_count(youtube, destination_id)
    available = MAX_PLAYLIST_ITEMS - destination_count
    logger.info(f"destination has {destination_count} items, {available} slots available")
    if available <= 0:
        logger.info("destination playlist is full, nothing to move")
        return
    source_items = get_all_items_from_playlist_ids(youtube, [source_id])
    logger.info(f"source has {len(source_items)} items")
    moved = 0
    to_move = min(available, len(source_items))
    logger.info(f"would move {to_move} videos")
    for item in source_items:
        if moved >= available:
            break
        if ConfigDelete.do_delete:
            video_id = item["snippet"]["resourceId"]["videoId"]
            add_video_to_playlist(youtube, destination_id, video_id)
            delete_playlist_item_by_id(youtube, item["id"])
        moved += 1
        log_progress(logger, moved, to_move)
    if ConfigDelete.do_delete:
        logger.info(f"moved {moved} videos from [{ConfigOverflow.source}] to [{ConfigOverflow.destination}]")
    else:
        logger.info(f"dry run: would move {moved} videos from [{ConfigOverflow.source}] to [{ConfigOverflow.destination}]")


@register_endpoint(
    description="Find unseen/seen videos by diffing playlists against local files",
    configs=[ConfigPagination, ConfigDiff],
)
def diff() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    playlist_video_ids = get_video_ids_from_playlist_names(youtube, ConfigDiff.source_playlists)
    file_video_ids = read_video_ids_from_files(ConfigDiff.seen_files)
    if ConfigDiff.reverse:
        result_ids = sorted(playlist_video_ids & file_video_ids)
    else:
        result_ids = sorted(playlist_video_ids - file_video_ids)
    logger.info(f"found {len(result_ids)} videos")
    with open(ConfigDiff.output_file, "w") as f:
        for video_id in result_ids:
            print(video_id, file=f)
    logger.info(f"wrote {len(result_ids)} video IDs to [{ConfigDiff.output_file}]")


@register_endpoint(
    description="Fetch extensive metadata for video IDs and write to CSV (supports resume)",
    configs=[ConfigAddData],
)
def add_data() -> None:
    logger = logging.getLogger()
    input_path = ConfigAddData.input_file
    output_path = ConfigAddData.output_csv
    processed_ids: set[str] = set()
    output_file_exists = os.path.exists(output_path)
    if output_file_exists:
        logger.info(f"Output file [{output_path}] found. Reading existing IDs to avoid re-processing.")
        with open(output_path, encoding="utf-8", newline="") as f_out_read:
            reader = csv.DictReader(f_out_read)
            for row in reader:
                if row and "video_id" in row:
                    processed_ids.add(row["video_id"])
        logger.info(f"Found {len(processed_ids)} previously processed IDs.")
    with open(input_path) as infile, open(output_path, "a", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=METADATA_FIELDNAMES)
        if not output_file_exists:
            writer.writeheader()
            outfile.flush()
        for line in infile:
            video_id = line.strip()
            if not video_id:
                continue
            if video_id in processed_ids:
                logger.info(f"Skipping already processed ID: [{video_id}]")
                continue
            metadata = get_video_metadata(video_id)
            if metadata:
                writer.writerow(metadata)
            else:
                error_row = {field: "" for field in METADATA_FIELDNAMES}
                error_row["video_id"] = video_id
                error_row["title"] = "METADATA_NOT_FOUND"
                writer.writerow(error_row)
            outfile.flush()
    logger.info("Processing complete")


@register_endpoint(
    description="Get info about a video",
    configs=[ConfigVideo],
)
def video_info() -> None:
    youtube = get_youtube()
    info = get_video_info(youtube, ConfigVideo.id)
    pretty_print(info)


YOUTUBE_ID_RE = re.compile(r"(?:youtu\.be/|youtube\.com/.*[?&]v=|^)([A-Za-z0-9_-]{11})(?:\s|$|&)")


@register_endpoint(
    description="Extract YouTube video IDs from text files",
    configs=[ConfigCollectIds],
)
def collect_ids() -> None:
    logger = logging.getLogger()
    found: set[str] = set()
    for file_path in ConfigCollectIds.collect_files:
        with open(str(file_path), encoding="utf-8", errors="ignore") as f:
            for line in f:
                for match in YOUTUBE_ID_RE.findall(line):
                    found.add(match)
    for video_id in sorted(found):
        print(video_id)
    logger.info(f"found {len(found)} unique video IDs")


@register_endpoint(
    description="Add video IDs from a file to a playlist",
    configs=[ConfigPagination, ConfigAddFileToPlaylist],
)
def add_file_to_playlist() -> None:
    logger = logging.getLogger()
    youtube = get_youtube()
    playlist_id = get_playlist_ids_from_names(youtube, [ConfigAddFileToPlaylist.add_playlist])[0]
    video_ids = read_video_ids_from_files([str(ConfigAddFileToPlaylist.add_file)])
    logger.info(f"read {len(video_ids)} video IDs from [{ConfigAddFileToPlaylist.add_file}]")
    added = 0
    total = len(video_ids)
    for video_id in sorted(video_ids):
        add_video_to_playlist(youtube, playlist_id, video_id)
        added += 1
        log_progress(logger, added, total)
    logger.info(f"added {added} videos to [{ConfigAddFileToPlaylist.add_playlist}]")


@register_endpoint(
    description="List channels",
)
def channels() -> None:
    youtube = get_youtube()
    channels_obj = get_youtube_channels(youtube)
    request = channels_obj.list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = retry_execute(request)
    pretty_print(response)
    for item in response["items"]:
        f_channel_id = item["id"]
        playlists_obj = get_youtube_playlists(youtube)
        request = playlists_obj.list(
            part="snippet,contentDetails",
            channelId=f_channel_id,
            maxResults=25
        )
        res = retry_execute(request)
        pretty_print(res)


@register_endpoint(
    description="Download Watch Later playlist",
)
def watch_later() -> None:
    youtube_dl_download_urls(["https://www.youtube.com/playlist?list=WL"])


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    ConfigRequest.scopes = SCOPES
    ConfigRequest.location = os.path.dirname(os.path.realpath(__file__))
    register_functions()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
