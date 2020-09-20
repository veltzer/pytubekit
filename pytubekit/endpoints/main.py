"""
main entry point to the program
"""


import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch

from pytubekit.endpoints.group_default import register_group_default


def register_all_groups():
    """
    registers all groups of operations with pytconf
    """
    register_group_default()


@register_main()
def main():
    """
    Pytubekit will allow you to perform operations in your youtube account en masse
    """
    pylogconf.core.setup()
    register_all_groups()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
