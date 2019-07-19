import re

from . import utils

NAME_VALID_CHARS = "A-Z0-9_"
NAME_VALID_STR = r"(?P<type>REQ|SPC|TST)-(?:[{0}]+-)*(?:[{0}]+)".format(
    NAME_VALID_CHARS)
NAME_VALID_RE = re.compile(r"^{}$".format(NAME_VALID_STR), re.IGNORECASE)

REQ = "REQ"
SPC = "SPC"
TST = "TST"


class Name(utils.KeyCmp):
    def __init__(self, key, ty, raw):
        super(Name, self).__init__(key=key.upper())
        self.ty = ty
        self.raw = raw

    @classmethod
    def from_str(cls, raw):
        if raw is None:
            raise ValueError("the str cannot be None")

        match = NAME_VALID_RE.match(raw)
        if not match:
            raise ValueError("Invalid name: {}".format(raw))

        return cls(key=raw.upper(), ty=match.group(1).upper(), raw=raw)

    def __repr__(self):
        return self.raw

    def serialize(self):
        return self.raw
