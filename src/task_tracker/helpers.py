"""
Contains the following functions:

* timestamp()
"""


def timestamp(seconds: int | float) -> str:
    """
    Takes seconds in the form `18221.51687` and returns a value
    of the form `05:03:42`.
    """
    (hours, seconds) = divmod(seconds, 3600)
    (minutes, seconds) = divmod(seconds, 60)
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
