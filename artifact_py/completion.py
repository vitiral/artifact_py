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

def impl_to_statistics(impl, subnames):
    """"
    Return the `(count, value, secondary_count, secondary_value)`
    that this impl should contribute to the "implemented" statistics.

    "secondary" is used because the Done field actually does contribute to
    both spc AND tst for REQ and SPC types.

    `subnames` should contain the subnames the artifact defines.
    """
    if impl is None:
        if subnames:
            # If subnames are defined not being implemented
            # in code means that you get counts against you
            (1 + len(subnames), 0.0, 0, 0.0)
        else:
            return (0, 0.0, 0, 0.0)
    if isinstance(impl, ImplDone):
        return (1, 1.0, 1, 1.0)
    if isinstance(impl, ImplCode):
        return _implcode_to_statistics(impl, subnames)
    else:
        raise TypeError(impl)


def _implcode_to_statistics(impl, subnames):
    count = 1
    value = int(bool(impl.primary))

    sec_count = 0
    sec_value = 0.0
    for sub in subnames:
        count += 1

        # track if the subname is implemented
        contains_key = int(sub in impl.secondary)
        value += contains_key

        if sub.is_tst():
            sec_count += 1
            sec_value += contains_key

    return (count, value, sec_count, sec_value)
