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


class ConfigDelete(Config):
    doit = ParamCreator.create_bool(
        help_string="Really delete?",
        default=True,
    )
