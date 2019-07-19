import os
import six

from . import utils


class Settings:
    def __init__(self, root_file, root_dir, code_paths, exclude_code_paths, extra):
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
        root_dir = utils.joinabs(
            os.path.dirname(root_file),
            dct.pop('root_dir', ''))
        code_paths = utils.joinabs_all(root_dir, dct.pop('code_paths', []))
        exclude_code_paths = utils.joinabs_all(root_dir, dct.pop('exclude_code_paths', []))

        return cls(
            root_file=root_file,
            root_dir=root_dir,
            code_paths=code_paths,
            exclude_code_paths=exclude_code_paths,
            extra=dct
        )

    def serialize(self):
        return {
            'root_dir': os.path.dirname(self.root_file),
            'code_paths': utils.relpath_all(self.root_dir, self.code_paths),
            'exclude_code_paths': utils.relpath_all(self.root_dir, self.exclude_code_paths),
            'extra': self.extra,
        }
