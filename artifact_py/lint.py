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
"""Module for linting a project's design docs."""
from __future__ import unicode_literals

import re
import six

import anchor_txt

from . import code
from . import dump
from .name import format_name

NAME_REF = r"\[{}\]".format(code.NAME_FULL_STR)
NAME_REF_RE = re.compile(NAME_REF, re.IGNORECASE)

PARTOF_DNE = "{} is partof {} which does not exist"
PARTOF_TST = "{} is partof {}. TST types cannot be partof non-TST types."
IMPL_MULTIPLE = "{} is implemented in code multiple times: {}"
IMPL_DONE = "{} is implemented in code and marked as done. Code impls: {}"
REF_INVALID = "{} is referenced in the design but does not exist."
REF_INVALID_SUBPART = "{} is referenced in the design but subpart {} does not exist."
PROJ_NOT_UPDATED = ("Design references are out of date. To fix run:"
                    " artifact_py export -i --format md")


def lint_project(project):
    """Lint the project, returning the failed lints."""
    lints = Lints(project)
    lints.lint_all()
    return lints


class Lints(object):
    """An object for building lints."""
    def __init__(self, project):
        self.project = project
        self.art_map = {art.name: art for art in project.artifacts}
        self.errors = []
        self.warnings = []

    def lint_all(self):
        """Run all lints."""
        self.lint_partof_exists()
        self.lint_partof_tst()
        self.lint_extra_impls()
        self.lint_done()
        self.lint_references()
        self.lint_export_md()

    def lint_partof_exists(self):
        """Lint that all `partof` values exist."""
        for art in self.project.artifacts:
            for partof in art.partof:
                if partof not in self.art_map:
                    self.errors.append(PARTOF_DNE.format(art.name, partof))

    def lint_partof_tst(self):
        """Lint whether a non-TST artifact is partof a TST one."""
        for art in self.project.artifacts:
            if art.name.is_tst():
                continue
            for partof in art.partof:
                if partof.is_tst():
                    self.errors.append(PARTOF_TST.format(art.name, partof))

    def lint_extra_impls(self):
        """Lint multiple impls if they are not supported."""
        for art in self.project.artifacts:
            if not isinstance(art.impl, code.ImplCode):
                continue
            if len(art.impl.primary) > 1:
                self.errors.append(
                    IMPL_MULTIPLE.format(
                        art.name, self._format_codelocs(art.impl.primary)))

            for sub, impls in six.iteritems(art.impl.secondary):
                if len(impls) > 1:
                    self.errors.append(
                        IMPL_MULTIPLE.format(format_name(art.name, sub),
                                             self._format_codelocs(impls)))

    def lint_done(self):
        """An artifact cannot be marked as `done` and implemented in code."""
        for art in self.project.artifacts:
            if isinstance(art.impl, code.ImplCode) and art.done:
                self.errors.append(
                    IMPL_DONE.format(art.name,
                                     self._format_codelocs_impl(art.impl)))

    def lint_references(self):
        """Lint references in the design doc."""
        for content in _all_contents(self.project.root_section):
            if not isinstance(content, anchor_txt.Text):
                continue
            for line in content.raw:
                for match in NAME_REF_RE.finditer(line):
                    name, subpart = code.name_from_match(match)

                    art = self.art_map.get(name)
                    if art is None:
                        self.warnings.append(REF_INVALID.format(
                            match.group(0)))
                        continue

                    if subpart and subpart not in art.subparts:
                        self.warnings.append(
                            REF_INVALID_SUBPART.format(match.group(0),
                                                       subpart))

    def lint_export_md(self):
        """Make sure that a new design doc shouldn't be exported."""
        correct = dump.dump_project(self.project)
        correct.append('')  # every write_line adds a newline
        correct = '\n'.join(correct)
        with open(self.project.settings.root_file) as proj_file:
            existing = proj_file.read()

        if correct != existing:
            self.warnings.append(PROJ_NOT_UPDATED)

    def _format_codelocs(self, locs):
        out = []
        for loc in locs:
            out.append(loc.to_str(self.project.settings))
        return ' '.join(out)

    def _format_codelocs_impl(self, impl):
        all_locs = []
        all_locs.extend(impl.primary)
        for locs in six.itervalues(impl.secondary):
            all_locs.extend(locs)
        return self._format_codelocs(all_locs)


def _all_contents(section):
    """Return the contents of a section as an iterator."""
    for content in section.contents:
        yield content

    for subsection in section.sections:
        for content in _all_contents(subsection):
            yield content
