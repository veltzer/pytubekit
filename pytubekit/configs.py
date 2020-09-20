"""
All configurations for pytubekit
"""
import os

from pytconf import Config, ParamCreator


class ConfigAuthFiles(Config):
    """
    Parameters for authentication files
    """

    client_secret = ParamCreator.create_existing_file(
        help_string="Where are the credentials?",
        default=os.path.expanduser("~/.config/pytubekit/client_secret.json"),
    )
    token = ParamCreator.create_str(
        help_string="Where will we store the user access token?",
        default=os.path.expanduser("~/.config/pytubekit/token.pickle"),
    )


class ConfigFix(Config):
    """
    Parameters about fixing data in the database
    """

    doit = ParamCreator.create_bool(help_string="Really fix the source?", default=True,)
