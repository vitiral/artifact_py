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
