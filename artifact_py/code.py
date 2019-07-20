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
import os

import six

from . import name
from .name import Name
from .name import SubPart
from . import utils

RE_NAME_KEY = "name"
RE_SUBPART_KEY = "subpart"

NAME_CODE_STR = r"#(?P<name>{})(:?\.(?P<subpart>{}))?".format(name.NAME_VALID_STR,
                                        name.SUB_PART_VALID_STR)

NAME_CODE_RE = re.compile(NAME_CODE_STR, re.I)
NAME_CODE_VALID_RE = re.compile("${}^".format(NAME_CODE_STR), re.I)


class ImplCode:
    """Implemented in code.

    primary: list of CodeLoc
    secondary: dict[SubPart, list[CodeLoc]]
    """
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary

    @classmethod
    def new(cls):
        return cls([], {})

    def insert_primary(self, codeloc):
        assert isinstance(codeloc, CodeLoc)
        self.primary.append(codeloc)

    def insert_secondary(self, subpart, codeloc):
        assert isinstance(subpart, name.SubPart)
        assert isinstance(codeloc, CodeLoc)
        if subpart not in self.secondary:
            self.secondary[subpart] = []
        self.secondary[subpart].append(codeloc)

    def serialize(self, settings):
        return {
            "primary": settings.serialize_list(self.primary),
            "secondary": {
                n.serialize(settings): settings.serialize_list(c)
                for n, c in six.iteritems(self.secondary)
            },
        }


class CodeLoc:
    def __init__(self, file_, line):
        self.file = file_
        self.line = line

    def serialize(self, settings):
        return {
            "file": settings.relpath(self.file),
            "line": self.line,
        }


def find_impls(settings):
    invalid = []
    impls = {}
    find_impls_recursive(
        invalid=invalid,
        impls=impls,
        code_paths=settings.code_paths,
        exclude_code_paths=settings.exclude_code_paths,
    )
    if invalid:
        raise ValueError("Paths do not exist: {}".format(invalid))
    return impls


def find_impls_recursive(invalid, impls, code_paths, exclude_code_paths):
    for code_path in code_paths:
        if is_excluded(code_path, exclude_code_paths):
            continue
        if not os.path.exists(code_path):
            invalid.append(code_path)
        elif os.path.isdir(code_path):
            for entry in os.listdir(code_path):
                find_impls_recursive(
                    invalid=invalid,
                    impls=impls,
                    code_paths=[os.path.join(code_path, entry)],
                    exclude_code_paths=exclude_code_paths,
                )
        else:
            update_impls_file(impls, code_path)


def is_excluded(path, exclude_code_paths):
    for exclude in exclude_code_paths:
        if path.startswith(exclude):
            return True
    return False


def update_impls_file(impls, code_file):
    with open(code_file) as fd:
        for linenum, line in enumerate(fd):
            update_impls_line(code_file, impls, linenum, line)


def update_impls_line(code_file, impls, linenum, line):
    for match in NAME_CODE_RE.finditer(line):
        codeloc = CodeLoc(code_file, line=linenum)
        groups = match.groupdict()
        name = Name.from_str(groups[RE_NAME_KEY])
        if name not in impls:
            impls[name] = ImplCode.new()

        subpart = groups.get(RE_SUBPART_KEY)
        if subpart:
            subpart = SubPart.from_str(subpart)
            impls[name].insert_secondary(subpart, codeloc)
        else:
            impls[name].insert_primary(codeloc)
