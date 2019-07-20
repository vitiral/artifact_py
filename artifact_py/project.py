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
import anchor_txt
import six

from . import utils


class Project:
    def __init__(self, settings, artifacts, contents, sections):
        self.settings = settings
        self.artifacts = artifacts
        self.sections = sections

    def serialize(self):
        return {
            "settings": self.settings.serialize(),
            "artifacts": self.settings.serialize_list(self.artifacts),
        }

    def to_lines(self):
        lines = []
        for section in self.sections:
            lines.extend(section.to_lines())
        for artifact in self.artifacts:
            lines.extend(artifact.to_lines())
        return lines
