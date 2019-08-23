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
"""A collection of utility functions and classes used throughout artifact_py."""
from __future__ import unicode_literals, division
import os
import sys

from collections import OrderedDict
import six
# this import is forwarded, so it is not unused - but the linter doesn't know!
from anchor_txt.utils import to_unicode # pylint: disable=unused-import


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
    """Get an absolute representation of a path, raising an error if it contains tilde expansion."""
    if '~' in path:
        raise ValueError("Path cannot use home directory '~'")
    return os.path.abspath(path)


def joinabs(path, sub_path):
    return abspath(os.path.join(path, sub_path))


def joinabs_all(root_dir, paths):
    return [joinabs(root_dir, p) for p in paths]


def ordered_recurse(value):
    """Recursively order nested dicts and lists at all levels."""
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
    """Write a collection to an output, separating each item with a line break."""
    for line in lines:
        output.write(line)
        output.write('\n')


def flush_output(output):
    """Flush, and force write to disk if not stdout/stderr, the given output buffer."""
    output.flush()
    if output not in (sys.stdout, sys.stderr):
        os.fsync(output)


def ensure_str(name, value, allow_none=False):
    """Raise an error if value is not a str and, optionally, is None."""
    if allow_none and value is None:
        return value

    if not isinstance(value, six.text_type):
        raise TypeError("{} must be str: {}".format(name, value))
    return value


def ensure_list(name, value, item_type=None):
    """Raise an error if value is not a list or, optionally, contains elements
    not of a specified type."""
    if not isinstance(value, list):
        raise TypeError("{} must be a list: {}".format(name, value))
    if item_type:
        for item in value:
            if not isinstance(item, item_type):
                raise TypeError("{} contain only {}: {}".format(
                    name, item_type, item))

    return value


def ratio(value, count):
    """compute ratio but ignore count=0"""
    if count == 0:
        return 0.0
    return value / count
