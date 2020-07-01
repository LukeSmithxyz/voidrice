

def to_bool(value):
    """Converts a String to a Boolean.

    Args:
        value (str or bool): a boolean or a string representing a boolean

    Returns:
        bool: the evaluated boolean
    """
    import distutils.util
    return (value if isinstance(value, bool)
            else bool(distutils.util.strtobool(value)))
