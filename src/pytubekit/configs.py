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
        help_string="What playlists to clean up",
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
    source_playlists = ParamCreator.create_list_str(
        help_string="YouTube playlist names to pull videos from",
    )
    seen_files = ParamCreator.create_list_str(
        help_string="Local files with video IDs (one per line, dump format)",
    )
    reverse = ParamCreator.create_bool(
        help_string="False = unseen videos, True = seen videos",
        default=False,
    )
    output_file = ParamCreator.create_str(
        help_string="Path to write results to",
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


class ConfigCopy(Config):
    """ Copy playlist parameters """
    copy_source = ParamCreator.create_str(
        help_string="Source playlist name to copy from",
    )
    copy_destination = ParamCreator.create_str(
        help_string="Destination playlist name to copy to",
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


class ConfigLeftToSee(Config):
    """ Left to see parameters """
    lts_all_playlists = ParamCreator.create_list_str(
        help_string="Playlist names containing all videos",
    )
    lts_seen_playlists = ParamCreator.create_list_str(
        help_string="Playlist names containing already-seen videos",
    )


class ConfigCount(Config):
    """ Playlists to count """
    count_names = ParamCreator.create_list_str(
        help_string="What playlists to count items in",
    )


class ConfigCollectIds(Config):
    """ Collect IDs parameters """
    collect_files = ParamCreator.create_list_str(
        help_string="Files to scan for YouTube video IDs",
    )


class ConfigPrint(Config):
    """ How to dump things """
    full = ParamCreator.create_bool(
        help_string="full dumps or just id?",
        default=False,
    )
