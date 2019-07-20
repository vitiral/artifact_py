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
from __future__ import unicode_literals, division
"""
For types and methods associated with the completion ratio of artifacts.
"""
import re
from . import utils
from . import name
from . import code


class Completion(utils.KeyCmp):
    def __init__(self, spc, tst):
        super(Completion, self).__init__(key=(spc, tst))
        self.spc = spc
        self.tst = tst

    def serialize(self, _settings):
        return {
            "spc": self.spc,
            "tst": self.tst,
        }


class ImplDone:
    def __init__(self, raw):
        self.raw = raw

    def serialize(self, _settings):
        return self.raw


def impl_to_statistics(impl, subparts):
    """"
    Return the `(count, value, secondary_count, secondary_value)` that this
    impl should contribute to the "specified" and "tested" statistics.

    "secondary" is used because the Done field actually does contribute to
    both spc AND tst for REQ and SPC types.

    `subparts` should contain the subparts the artifact defines.
    """
    if impl is None:
        if subparts:
            # If subparts are defined not being implemented
            # in code means that you get counts against you
            return (1 + len(subparts), 0.0, 0, 0.0)
        else:
            return (0, 0.0, 0, 0.0)
    if isinstance(impl, ImplDone):
        return (1, 1.0, 1, 1.0)
    if isinstance(impl, code.ImplCode):
        return _implcode_to_statistics(impl, subparts)
    else:
        raise TypeError(impl)


def _implcode_to_statistics(impl, subparts):
    count = 1
    value = int(bool(impl.primary))

    sec_count = 0
    sec_value = 0.0
    for sub in subparts:
        count += 1

        # track if the subname is implemented
        contains_key = int(sub in impl.secondary)
        value += contains_key

        if sub.is_tst():
            sec_count += 1
            sec_value += contains_key

    return (count, value, sec_count, sec_value)
