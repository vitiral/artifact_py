import copy

import anchor_txt
import networkx as nx

from . import settings
from . import project
from . import artifact
from . import name


def from_root_file(root_file):
    root_section = anchor_txt.Section.from_md_path(root_file)
    p_settings = settings.Settings.from_dict(
        root_section.attributes.get('artifact', {}), root_file)
    project_sections = load_project_sections(
        sections=root_section.sections,
        file_=root_file,
    )
    artifacts = load_artifacts(
        project_sections=project_sections,
        settings=p_settings,
    )
    return project.Project(
        settings=p_settings,
        artifacts=artifacts,
        contents=root_section.contents,
        sections=project_sections,
    )


def load_project_sections(sections, file_):
    """Load artifacts from the sections.
    """

    # project sections can either be:
    # - a raw section
    # - an ArtifactBuilder, which contains a section
    project_sections = []

    for section in sections:
        try:
            art_name = name.Name.from_str(section.header.anchor)
        except ValueError:
            project_sections.append(section)
            continue

        art_im = artifact.ArtifactBuilder.from_attributes(
            attributes=section.attributes,
            section=section,
            name=art_name,
            file_=file_)

        project_sections.append(art_im)

    return project_sections


def load_artifacts(project_sections, settings):
    graph = nx.DiGraph()

    builders = [
        s for s in project_sections if isinstance(s, artifact.ArtifactBuilder)
    ]
    # for art in builders:
    #     graph.add_nodes(art.name)

    #     for part in art.partof:
    #         graph.add_edge(part, art.name)

    return {art.name: art.build(settings) for art in builders}
