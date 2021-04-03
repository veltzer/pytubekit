"""
All configurations
"""
from pytconf import Config, ParamCreator


class ConfigPagination(Config):
    page_size = ParamCreator.create_int(
        help_string="What page size to use for pagination (max is 50)",
        # if you set it for more than 50 it will be 50...
        default=50,
    )


class ConfigPlaylist(Config):
    name = ParamCreator.create_str(
        help_string="What playlist to use",
    )


class ConfigVideo(Config):
    id = ParamCreator.create_str(
        help_string="Video id to use",
    )


class ConfigPlaylists(Config):
    names = ParamCreator.create_list_str(
        help_string="What playlists to use",
    )


class ConfigCleanup(Config):
    dedup = ParamCreator.create_bool(
        help_string="Really delete duplicates?",
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


class ConfigDump(Config):
    full = ParamCreator.create_bool(
        help_string="full dumps or just id?",
        default=False,
    )
