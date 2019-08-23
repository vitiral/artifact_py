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

import six

from . import code
from .name import format_name

PARTOF_DNE = "{} is partof {} which does not exist"
PARTOF_TST = "{} is partof {}. TST types cannot be partof non-TST types."
IMPL_MULTIPLE = "{} is implemented in code multiple times: {}"


def lint_project(project):
    """Lint the project, returning the failed lints."""
    lints = Lints(project)
    lints.lint_all()
    return lints


class Lints(object):
    """An object for building lints."""
    def __init__(self, project):
        self.project = project
        self.names = {art.name for art in project.artifacts}
        self.errors = []
        self.warnings = []

    def lint_all(self):
        """Run all lints."""
        self.lint_partof_exists()
        self.lint_partof_tst()
        self.lint_extra_impls()

    def lint_partof_exists(self):
        """Lint that all `partof` values exist."""
        for art in self.project.artifacts:
            for partof in art.partof:
                if partof not in self.names:
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

    def _format_codelocs(self, locs):
        out = []
        for loc in locs:
            out.append(loc.to_str(self.project.settings))
        return ' '.join(out)
