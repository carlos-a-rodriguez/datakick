"""
datakick.exceptions
-------------------

This module contains the set of datakick's exceptions.

"""


class ImageTooLargeError(Exception):
    """The image was too large."""


class InvalidImageFormatError(Exception):
    """The image extension was not one of the approved extensions."""