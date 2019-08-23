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
"""Project class."""

from __future__ import unicode_literals


class Project(object):
    """Encapsulates an entire project.

    Includes the settings, design (artifacts) and code impls.
    """
    def __init__(self, settings, artifacts, root_section, impls):
        self.settings = settings
        self.artifacts = artifacts
        self.root_section = root_section
        self.impls = impls

    def serialize(self):
        # TODO: dump the sections+contents
        return {
            "settings": self.settings.serialize(),
            "artifacts": self.settings.serialize_list(self.artifacts),
        }

    def to_lines(self):
        return self.root_section.to_lines()
