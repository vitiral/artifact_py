import os


class KeyCmp(object):
    """An object which is key comparable."""
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def _cmp(self, other):
        if self.key == other.key:
            return 0
        elif self.key < other.key:
            return -1
        else:
            return 1

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ne__(self, other):
        return self._cmp(other) != 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __gt__(self, other):
        return self._cmp(other) > 0


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


