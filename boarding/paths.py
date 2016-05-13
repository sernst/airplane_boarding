import json
import logging
import os
import typing

MY_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def package(*args: typing.List[str]) -> str:
    """
    Create an absolute path within the boarding project from the relative
    pieces specified in the args list

    :param args:
        String path components
    """

    return os.path.abspath(os.path.join(MY_DIRECTORY, '..', *args))

