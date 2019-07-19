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
import os
import six

from . import utils


class Settings:
    def __init__(self, root_file, root_dir, code_paths, exclude_code_paths,
                 extra):
        self.root_file = root_file
        self.root_dir = root_dir
        self.code_paths = code_paths
        self.exclude_code_paths = exclude_code_paths
        self.extra = extra

    @classmethod
    def from_dict(cls, dct, root_file):
        return cls.from_dict_consume(dict(dct), root_file)

    @classmethod
    def from_dict_consume(cls, dct, root_file):
        root_dir = utils.joinabs(os.path.dirname(root_file),
                                 dct.pop('root_dir', ''))
        code_paths = utils.joinabs_all(root_dir, dct.pop('code_paths', []))
        exclude_code_paths = utils.joinabs_all(
            root_dir, dct.pop('exclude_code_paths', []))

        return cls(root_file=root_file,
                   root_dir=root_dir,
                   code_paths=code_paths,
                   exclude_code_paths=exclude_code_paths,
                   extra=dct)

    def relpath(self, path):
        """Get the relative path from the settings root."""
        return utils.to_unicode(os.path.relpath(path, start=self.root_dir))

    def relpath_all(self, paths):
        """Return the relative paths to the root directory."""
        return [self.relpath(p) for p in paths]

    def serialize_list(self, lst):
        return [v.serialize(self) for v in lst]

    def serialize_list(self, lst):
        return [v.serialize(self) for v in lst]

    def serialize_maybe(self, value):
        if value is None:
            return value
        return value.serialize(self)

    def serialize(self):
        return {
            'root_dir': os.path.dirname(self.root_file),
            'code_paths': self.relpath_all(self.code_paths),
            'exclude_code_paths': self.relpath_all(self.exclude_code_paths),
            'extra': self.extra,
        }
