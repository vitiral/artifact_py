
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

