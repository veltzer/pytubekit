"""
All configurations
"""
from pytconf import Config, ParamCreator


class ConfigPlaylist(Config):
    playlist = ParamCreator.create_str(
        help_string="What playlist to use",
    )
