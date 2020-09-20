"""
This is a generic object dumper for debugging purposes.
It's funny I have not found a good implementation of this...
See the links for discussions of this topic.

References:
- https://stackoverflow.com/questions/192109/\
    is-there-a-built-in-function-to-print-all-the-current-properties-and-values-of-a
- https://gist.github.com/passos/1071857
"""


import json
import sys


def object_to_members_or_string(obj):
    if hasattr(obj, "__dict__"):
        return vars(obj)
    return str(obj)


def flat_dump(obj) -> None:
    """
    Dump object to stdout. Only dumps the immediate members of the object
    :param obj:
    """
    json.dump(
        vars(obj), fp=sys.stdout, default=object_to_members_or_string, indent=1,
    )


def dump(obj) -> None:
    json.dump(
        vars(obj), fp=sys.stdout, default=object_to_members_or_string, indent=1,
    )
