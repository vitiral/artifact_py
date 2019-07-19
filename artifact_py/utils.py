import os


class KeyCmp(object):
    """An object which is key comparable."""
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(type(other))
        return self.key.__cmp__(other.key)


def abspath(path):
    if '~' in path:
        raise ValueError("Path cannot use home directory '~'")
    return os.path.abspath(path)


def joinabs(a, b):
    return abspath(os.path.join(a, b))


def joinabs_all(root_dir, paths):
    return [joinabs(root_dir, p) for p in paths]


def serialize_list(lst):
    return [v.serialize() for v in lst]


def serialize(value):
    if value is None:
        return value
    return value.serialize()


