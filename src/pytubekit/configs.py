"""
All configurations
"""
from pytconf import Config, ParamCreator


class ConfigPagination(Config):
    """ Pagination parameters """
    page_size = ParamCreator.create_int(
        help_string="What page size to use for pagination (max is 50)",
        # if you set it for more than 50 it will be 50...
        default=50,
    )


class ConfigChannelId(Config):
    """ Channel ID options """
    watch_later = ParamCreator.create_bool(
        help_string="Output Watch Later playlist ID instead of channel ID",
        default=False,
    )


class ConfigDump(Config):
    """ Parameters for dumping """
    dump_folder = ParamCreator.create_str(
        help_string="Which folder to dump to",
        default=".",
    )


class ConfigSubtract(Config):
    """ Subtract parameters """
    subtract_what = ParamCreator.create_list_str(
        help_string="What playlists to subtract",
    )
    subtract_from = ParamCreator.create_list_str(
        help_string="What playlist to subtract from",
    )


class ConfigPlaylist(Config):
    """ Playlist parameters """
    name = ParamCreator.create_str_or_none(
        help_string="What playlist name to use",
        default=None,
    )
    playlist_id = ParamCreator.create_str_or_none(
        help_string="What playlist id to use",
        default=None,
    )


class ConfigVideo(Config):
    """ Video id to use """
    id = ParamCreator.create_str(
        help_string="Video id to use",
    )


class ConfigPlaylists(Config):
    """ Playlists to use """
    names = ParamCreator.create_list_str(
        help_string="What playlists to use",
    )


class ConfigCleanupPlaylists(Config):
    """ Playlists to clean up """
    cleanup_names = ParamCreator.create_list_str(
        help_string="What playlists to clean up (omit for all)",
        default=[],
    )


class ConfigDelete(Config):
    """ Configs for doing delete """
    do_delete = ParamCreator.create_bool(
        help_string="Really delete?",
        default=True,
    )


class ConfigCleanup(Config):
    """ Parameters for cleanup """
    dedup = ParamCreator.create_bool(
        help_string="detect duplicates?",
        default=True,
    )
    deleted = ParamCreator.create_bool(
        help_string="Really delete deleted?",
        default=True,
    )
    privatized = ParamCreator.create_bool(
        help_string="Really delete privatized?",
        default=True,
    )


class ConfigDiff(Config):
    """ Parameters for diff """
    diff_a_playlists = ParamCreator.create_list_str(
        help_string="Source A: YouTube playlist names",
        default=[],
    )
    diff_a_files = ParamCreator.create_list_str(
        help_string="Source A: local files with video IDs",
        default=[],
    )
    diff_b_playlists = ParamCreator.create_list_str(
        help_string="Source B: YouTube playlist names",
        default=[],
    )
    diff_b_files = ParamCreator.create_list_str(
        help_string="Source B: local files with video IDs",
        default=[],
    )
    diff_reverse = ParamCreator.create_bool(
        help_string="False = A-B (difference), True = A&B (intersection)",
        default=False,
    )
    diff_output_file = ParamCreator.create_str_or_none(
        help_string="Path to write results to (omit for stdout)",
        default=None,
    )


class ConfigAddData(Config):
    """ Parameters for add_data """
    input_file = ParamCreator.create_str(
        help_string="Path to text file with video IDs (one per line)",
    )
    output_csv = ParamCreator.create_str(
        help_string="Path to CSV file to write metadata to",
    )


class ConfigOverflow(Config):
    """ Overflow parameters """
    source = ParamCreator.create_str(
        help_string="Source playlist name",
    )
    destination = ParamCreator.create_str(
        help_string="Destination playlist name",
    )


class ConfigClear(Config):
    """ Playlist to clear """
    clear_name = ParamCreator.create_str(
        help_string="Name of playlist to clear",
    )


class ConfigMerge(Config):
    """ Merge parameters """
    merge_sources = ParamCreator.create_list_str(
        help_string="Source playlist names to merge from",
    )
    merge_destination = ParamCreator.create_str(
        help_string="Destination playlist name to merge into",
    )
    merge_dedup = ParamCreator.create_bool(
        help_string="Skip duplicates already in destination",
        default=True,
    )


class ConfigSort(Config):
    """ Sort playlist parameters """
    sort_playlist_name = ParamCreator.create_str(
        help_string="Name of playlist to sort",
    )
    sort_key = ParamCreator.create_str(
        help_string="Sort key: title, channel, or date",
        default="title",
    )


class ConfigSearch(Config):
    """ Search playlist parameters """
    search_playlists = ParamCreator.create_list_str(
        help_string="Playlist names to search in",
    )
    search_query = ParamCreator.create_str(
        help_string="Text to search for in video title or channel name",
    )


class ConfigExportCsv(Config):
    """ Export playlist to CSV parameters """
    export_playlist_name = ParamCreator.create_str(
        help_string="Name of playlist to export",
    )
    export_csv_path = ParamCreator.create_str(
        help_string="Path to CSV file to write",
    )


class ConfigRename(Config):
    """ Rename playlist parameters """
    rename_playlist_name = ParamCreator.create_str(
        help_string="Current name of the playlist to rename",
    )
    rename_new_name = ParamCreator.create_str(
        help_string="New name for the playlist",
    )


class ConfigCollectIds(Config):
    """ Collect IDs parameters """
    collect_files = ParamCreator.create_list_str(
        help_string="Files to scan for YouTube video IDs",
    )


class ConfigAddFileToPlaylist(Config):
    """ Add videos from a file to a playlist """
    add_file = ParamCreator.create_str(
        help_string="Path to text file with video IDs (one per line)",
    )
    add_playlist = ParamCreator.create_str(
        help_string="Name of playlist to add videos to",
    )


class ConfigCreatePlaylist(Config):
    """ Create playlist parameters """
    create_name = ParamCreator.create_str(help_string="Name for the new playlist")
    create_description = ParamCreator.create_str(help_string="Description for the new playlist", default="")
    create_privacy = ParamCreator.create_str(help_string="Privacy status: public, unlisted, or private", default="public")


class ConfigDeletePlaylist(Config):
    """ Delete playlist parameters """
    delete_playlist_name = ParamCreator.create_str(help_string="Name of the playlist to delete")


class ConfigFindVideo(Config):
    """ Find video parameters """
    find_video_id = ParamCreator.create_str(help_string="Video ID to search for across all playlists")


class ConfigStatsFilter(Config):
    """ Optional filter for stats command """
    stats_names = ParamCreator.create_list_str(
        help_string="Filter to these playlist names (omit for all)",
        default=[],
    )


class ConfigLocalDumpFolder(Config):
    """ Local dump folder to operate on """
    local_dump_folder = ParamCreator.create_str(
        help_string="Path to dump folder",
        default=".",
    )


class ConfigLocalDiff(Config):
    """ Local diff parameters """
    local_diff_a = ParamCreator.create_str(
        help_string="Path A (file or folder)",
    )
    local_diff_b = ParamCreator.create_str(
        help_string="Path B (file or folder)",
    )
    local_diff_reverse = ParamCreator.create_bool(
        help_string="False = A-B (difference), True = A&B (intersection)",
        default=False,
    )



class ConfigPrint(Config):
    """ How to dump things """
    full = ParamCreator.create_bool(
        help_string="full dumps or just id?",
        default=False,
    )
