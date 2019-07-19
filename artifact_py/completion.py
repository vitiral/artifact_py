"""
For types and methods associated with the completion ratio of artifacts.
"""
from . import utils
from . import name

SUB_PART_VALID_RE = re.compile(
    r"^(?:tst-)?[{}]+$".format(name.NAME_VALID_CHARS), re.IGNORECASE)


class SubPart(utils.KeyCmp):
    def __init__(self, key, raw):
        super(SubPart, self).__init__(key=key)
        self.raw = raw

    def is_tst(self):
        return self.key.startswith("TST")

    @classmethod
    def from_str(cls, raw):
        match = SUB_NAME_VALID_RE.match(raw)
        if not match:
            raise ValueError("Invalid subparts: {}".format(raw))

        return cls(key=raw.upper(), raw)

    def __repr__(self):
        return self.raw


class Done:
    def __init__(self):
        pass
