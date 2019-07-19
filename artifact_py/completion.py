"""
For types and methods associated with the completion ratio of artifacts.
"""
import re
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
        match = SUB_PART_VALID_RE.match(raw)
        if not match:
            raise ValueError("Invalid subparts: {}".format(raw))

        return cls(key=raw.upper(), raw=raw)

    def __repr__(self):
        return self.raw

    def serialize(self, _settings):
        return self.raw


class ImplDone:
    def __init__(self, raw):
        self.raw = raw

    def serialize(self, _settings):
        return self.raw

class ImplCode:
    """Implemented in code.

    primary: CodeLoc or None
    secondary: dict[SubPart, CodeLoc]
    """

    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary

    def serialize(self, settings):
        return {
            "primary": settings.serialize_maybe(self.primary),
            "secondary": {
                n.serialize(settings): c.serialize(settings)
                for n, c in six.itervalues(self.secondary)

            },
        }

class CodeLoc:
    def __init__(self, settings, file_, line):
        self._settings = settings
        self.file = file_
        self.line = line

    def serialize(self, settings):
        return {
            "file": settings.relpath(self.file),
            "line": self.line,
        }
