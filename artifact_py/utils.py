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
import os
import sys

from collections import OrderedDict
import six
from anchor_txt.utils import to_unicode


class KeyCmp(object):
    """An object which is key comparable."""
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def _cmp(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)
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


def ordered_recurse(value):
    if isinstance(value, list):
        return [ordered_recurse(v) for v in value]
    if isinstance(value, dict):
        items = sorted(
            ((key, ordered_recurse(value))
             for key, value in six.iteritems(value)),
            key=lambda i: i[0],
        )
        return OrderedDict(items)

    return value


def write_lines(lines, output):
    for line in lines:
        output.write(line)
        output.write('\n')


def flush_output(output):
    output.flush()
    if output not in (sys.stdout, sys.stderr):
        os.fsync(output)


def ensure_str(name, value, allow_none=False):
    if allow_none and value is None:
        return value

    if not isinstance(value, six.text_type):
        raise TypeError("{} must be str: {}".format(name, value))
    return value


def ensure_list(name, value, itemtype=None):
    if not isinstance(value, list):
        raise TypeError("{} must be a list: {}".format(name, value))
    if itemtype:
        for item in value:
            if not isinstance(item, itemtype):
                raise TypeError("{} contain only {}: {}".format(
                    name, itemtype, item))

    return value


def ratio(value, count):
    """compute ratio but ignore count=0"""
    if count == 0:
        return 0.0
    else:
        return value / count
