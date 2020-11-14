"""
All configurations for pytubekit
"""
from pytconf import Config, ParamCreator


class ConfigAuth(Config):
    force = ParamCreator.create_bool(
        help_string="Should we force creation of a new auth token",
        default=False,
    )
    # parameters passed to run_local_server
    host = ParamCreator.create_str(
        help_string="The hostname for the local redirect server. This will be served over http, not https.",
        default='localhost',
    )
    port = ParamCreator.create_int(
        help_string="The port for the local redirect server.",
        # default=8080,
        default=0,
    )
    # noinspection PyProtectedMember
    authorization_prompt_message = ParamCreator.create_str(
        help_string="The message to display to tell the user to navigate to the authorization URL.",
        # default=InstalledAppFlow._DEFAULT_AUTH_PROMPT_MESSAGE,
        default="",
    )


class ConfigPlaylist(Config):
    playlist = ParamCreator.create_str(
        help_string="What playlist to use",
    )
