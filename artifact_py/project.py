import anchor_txt

from . import utils


class Project:
    def __init__(self, settings, artifacts):
        self.settings = settings
        self.artifacts = artifacts

    def serialize(self):
        return {
            "settings": self.settings.serialize(),
            "artifacts": utils.serialize_list(self.artifacts),
        }
