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
"""Module for artifact document settings"""
from __future__ import unicode_literals
import os
import six

from . import utils


# code_url = "https://github.com/vitiral/artifact/blob/master/{file}#L{line}"
class Settings:
    """
    The settings which define how to load the artifacts and how to create url
    links.

    See #SPC-design.settings

    """
    def __init__(self, root_file, root_dir, code_paths, exclude_code_paths,
                 code_url, extra):
        self.root_file = root_file
        self.root_dir = root_dir
        self.code_paths = code_paths
        self.exclude_code_paths = exclude_code_paths
        self.code_url = code_url
        self.extra = extra

    @classmethod
    def from_dict(cls, dct, root_file):
        return cls.from_dict_consume(dict(dct), root_file)

    @classmethod
    def from_dict_consume(cls, dct, root_file):
        root_dir = utils.ensure_str('root_dir', dct.pop('root_dir', ''))
        root_dir = utils.joinabs(os.path.dirname(root_file), root_dir)

        code_paths = utils.ensure_list(
            'code_paths',
            dct.pop('code_paths', []),
            item_type=six.text_type,
        )
        code_paths = utils.joinabs_all(root_dir, code_paths)

        exclude_code_paths = utils.ensure_list(
            'exclude_code_paths',
            dct.pop('exclude_code_paths', []),
            item_type=six.text_type,
        )
        exclude_code_paths = utils.joinabs_all(root_dir, exclude_code_paths)

        code_url = utils.ensure_str('code_url',
                                    dct.pop('code_url', None),
                                    allow_none=True)

        return cls(root_file=root_file,
                   root_dir=root_dir,
                   code_paths=code_paths,
                   exclude_code_paths=set(exclude_code_paths),
                   code_url=code_url,
                   extra=dct)

    def relpath(self, path):
        """Get the relative path from the settings root."""
        return utils.to_unicode(os.path.relpath(path, start=self.root_dir))

    def relpath_all(self, paths):
        """Return the relative paths to the root directory."""
        return [self.relpath(p) for p in paths]

    def serialize_list(self, lst):
        return [v.serialize(self) for v in lst]

    def serialize_maybe(self, value):
        if value is None:
            return value
        return value.serialize(self)

    def serialize(self):
        return {
            'root_dir': os.path.dirname(self.root_file),
            'code_paths': sorted(self.relpath_all(self.code_paths)),
            'exclude_code_paths':
            sorted(self.relpath_all(self.exclude_code_paths)),
            'code_url': self.code_url,
            'extra': self.extra,
        }
