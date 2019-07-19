import anchor_txt

from .settings import Settings
from .project import Project


def from_root_file(root_file):
    section = anchor_txt.Section.from_md_path(root_file)
    settings = Settings.from_dict(section.attributes.get('artifact', {}),
                                  root_file)
    artifacts = []  # TODO
    return Project(settings=settings, artifacts=artifacts)


def load_artifacts(settings, artifacts, sections):
    """Load artifacts from the sections, mutating them as we go.
    """
    pass
