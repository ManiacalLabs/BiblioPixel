def class_name(c):
    """
    :param c: either an object or a class
    :return: the classname as a string
    """
    if not isinstance(c, type):
        c = type(c)

    return '%s.%s' % (c.__module__, c.__name__)
