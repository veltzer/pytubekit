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


class ConfigPlaylist(Config):
    """ Playlist parameters """
    name = ParamCreator.create_str(
        help_string="What playlist to use",
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


class ConfigCleanup(Config):
    """ Parameters for cleanup """
    do_delete = ParamCreator.create_bool(
        help_string="Really delete?",
        default=True,
    )
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


class ConfigPrint(Config):
    """ How to dump things """
    full = ParamCreator.create_bool(
        help_string="full dumps or just id?",
        default=False,
    )
