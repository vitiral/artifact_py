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
"""Contains functionality related to the naming of Artifacts."""
from __future__ import unicode_literals
import re

from . import utils

NAME_VALID_CHARS = "A-Z0-9_"
NAME_VALID_STR = r"(?P<type>REQ|SPC|TST)-(?:[{0}]+-)*(?:[{0}]+)".format(
    NAME_VALID_CHARS)
NAME_VALID_RE = re.compile(r"^{}$".format(NAME_VALID_STR), re.IGNORECASE)

SUB_PART_VALID_STR = r"(?:tst-)?[{}]+".format(NAME_VALID_CHARS)
SUB_PART_VALID_RE = re.compile(r"^{}$".format(SUB_PART_VALID_STR),
                               re.IGNORECASE)

REQ = "REQ"
SPC = "SPC"
TST = "TST"


def format_name(name, subpart=None):
    """Return the proper string format of the name"""
    if subpart is None:
        return name.raw
    return '{}.{}'.format(name.raw, subpart.raw)


class Name(utils.KeyCmp):
    """Representation of the name of an Artifact."""
    def __init__(self, key, art_type, raw):
        super(Name, self).__init__(key=key.upper())
        self.art_type = art_type
        self.raw = raw

    @classmethod
    def from_str(cls, raw):
        """Generate a Name from raw text."""
        if raw is None:
            raise ValueError("the str cannot be None")

        match = NAME_VALID_RE.match(raw)
        if not match:
            raise ValueError("Invalid name: {}".format(raw))

        return cls(key=raw.upper(), art_type=match.group(1).upper(), raw=raw)

    def is_req(self):
        return self.art_type == REQ

    def is_spc(self):
        return self.art_type == SPC

    def is_tst(self):
        return self.art_type == TST

    def __repr__(self):
        return self.raw

    def serialize(self, _s):
        return self.raw


class SubPart(utils.KeyCmp):
    """Representation of an Artifact SubPart"""
    def __init__(self, key, raw):
        super(SubPart, self).__init__(key=key)
        self.raw = raw

    def is_tst(self):
        return self.key.startswith("TST")

    @classmethod
    def from_str(cls, raw):
        """Generate a SubPart from raw text."""
        match = SUB_PART_VALID_RE.match(raw)
        if not match:
            raise ValueError("Invalid subparts: {}".format(raw))

        return cls(key=raw.upper(), raw=raw)

    def __repr__(self):
        return self.raw

    def serialize(self, _settings):
        return self.raw
