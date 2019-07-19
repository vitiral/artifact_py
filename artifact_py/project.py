import anchor_txt

from . import utils


class Project:
    def __init__(self, settings, artifacts, contents, sections):
        self.settings = settings
        self.artifacts = artifacts
        self.sections = sections

    def serialize(self):
        return {
            "settings": self.settings.serialize(),
            "artifacts": utils.serialize_list(self.artifacts),
        }
