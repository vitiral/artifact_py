import os
import six

from . import utils


class Settings:
    def __init__(self, root_dir, code_paths, exclude_code_paths, extra):
        self.root_dir = root_dir
        self.code_paths = code_paths
        self.exclude_code_paths = exclude_code_paths
        self.extra = extra

    @classmethod
    def from_dict_consume(self, dct, file_path):
        root_dir = utils.joinabs(
            os.path.dirname(file_path),
            dct.pop('root_dir', ''))
        code_paths = utils.joinabs_all(root_dir, dct.pop('code_paths', []))
        exclude_code_paths = utils.joinabs_all(root_dir, dct.pop('exclude_code_paths', []))

        return cls(
            root_dir=root_dir,
            code_paths=code_paths,
            exclude_code_paths=exclude_code_paths,
            extra=dct
        )
