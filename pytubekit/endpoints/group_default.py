"""
The default group of operations that pytubekit has
"""
from pytconf import register_endpoint, register_function_group

import pytubekit
import pytubekit.version

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pytubekit commands"

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
]
APP_NAME = "pytubekit"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(group=GROUP_NAME_DEFAULT, )
def version() -> None:
    """
    Print version
    """
    print(pytubekit.version.VERSION_STR)
