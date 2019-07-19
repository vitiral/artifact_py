# artifact_py: the design documentation tool made for everyone.
#
# Copyright (C) 2019 Rett Berg <github.com/vitiral>
#
# The source code is Licensed under either of
#
# * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
#   http://www.apache.org/licenses/LICENSE-2.0)
# * MIT license ([LICENSE-MIT](LICENSE-MIT) or
#   http://opensource.org/licenses/MIT)
#
# at your option.
#
# Unless you explicitly state otherwise, any contribution intentionally submitted
# for inclusion in the work by you, as defined in the Apache-2.0 license, shall
# be dual licensed as above, without any additional terms or conditions.
from __future__ import unicode_literals
import re

from . import utils

NAME_VALID_CHARS = "A-Z0-9_"
NAME_VALID_STR = r"(?P<type>REQ|SPC|TST)-(?:[{0}]+-)*(?:[{0}]+)".format(
    NAME_VALID_CHARS)
NAME_VALID_RE = re.compile(r"^{}$".format(NAME_VALID_STR), re.IGNORECASE)


SUB_PART_VALID_STR = r"(?:tst-)?[{}]+".format(NAME_VALID_CHARS)
SUB_PART_VALID_RE = re.compile(r"^{}$".format(SUB_PART_VALID_STR), re.IGNORECASE)


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

    def serialize(self, _s):
        return self.raw


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
