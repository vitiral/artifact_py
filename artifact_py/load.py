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
"""Module for loading projects from a root file."""
from __future__ import unicode_literals, division

import anchor_txt
import networkx as nx

from . import settings
from . import project
from . import artifact
from . import name
from . import code
from . import completion
from . import utils

SETTINGS_KEY = 'artifact'


class ProjectBuilder(object):
    """Loads a project."""
    def __init__(self, root_file, root_section):
        self.root_file = root_file
        self.root_section = root_section
        self.settings = None
        self.impls = None
        self.builders = []
        self.builder_map = None
        self.graph = None

    def try_add_builder(self, section):
        """Attempt to add an artifact builder.

        If it does not have a valid header, ignore.
        """
        if not section.header:
            # root section is not an artifact
            return

        try:
            art_name = name.Name.from_str(section.header.anchor)
        except ValueError:
            # no valid anchor, not an artifact
            return

        builder = artifact.ArtifactBuilder.from_attributes(
            attributes=section.attributes,
            name=art_name,
            file_=self.root_file,
        )

        self.builders.append(builder)

    def update_builder_map(self):
        self.builder_map = {b.name: b for b in self.builders}

    def set_settings(self, proj_settings):
        if self.settings:
            raise ValueError("two settings found at " + self.root_file)
        self.settings = proj_settings

    def set_impls(self, impls):
        self.impls = impls

        for builder in self.builders:
            impl = impls.get(builder.name)
            if impl:
                builder.set_impl(impl)

    def set_graph(self, graph):
        self.graph = graph

    def build(self):
        """Build the project from the values set."""
        assert self.settings is not None
        assert self.impls is not None
        assert self.builder_map is not None
        assert self.graph is not None

        artifacts = [b.build() for b in self.builders]

        return project.Project(settings=self.settings,
                               artifacts=artifacts,
                               root_section=self.root_section,
                               impls=self.impls)


def from_root_file(root_file):
    """Load a project from a root file."""
    root_section = anchor_txt.Section.from_md_path(root_file)
    project_builder = _load_project_builder(root_section, root_file)

    proj_settings = find_settings(root_section, root_file)

    project_builder.set_impls(code.find_impls(proj_settings))

    load_graph_and_parts(project_builder)
    update_completion(project_builder)

    return project_builder.build()


def _load_project_builder(root_section, root_file):
    project_builder = ProjectBuilder(root_file=root_file,
                                     root_section=root_section)
    _recurse_section(project_builder, root_section)
    if not project_builder.settings:
        project_builder.settings = settings.Settings.from_dict(
            {},
            root_file,
        )
    project_builder.update_builder_map()
    return project_builder


def _recurse_section(project_builder, section):
    try_settings = try_get_settings(section, project_builder.root_file)
    if try_settings:
        project_builder.set_settings(try_settings)

    project_builder.try_add_builder(section)

    for child in section.sections:
        _recurse_section(project_builder, child)


def try_get_settings(section, root_file):
    if SETTINGS_KEY in section.attributes:
        return settings.Settings.from_dict(section.attributes[SETTINGS_KEY],
                                           root_file)
    return None


def find_settings(section, root_file):
    out = _find_settings_recurse(section, root_file)
    if out is None:
        return settings.Settings.from_dict({}, root_file)
    return out


def _find_settings_recurse(section, root_file):
    """Walk through all sections looking for the artifact settings."""
    if SETTINGS_KEY in section.attributes:
        return settings.Settings.from_dict(section.attributes[SETTINGS_KEY],
                                           root_file)

    for sec in section.sections:
        out = _find_settings_recurse(sec, root_file)
        if out:
            return out

    return None


def load_graph_and_parts(project_builder):
    """Load the relationship graph of the artifacts and set their parts."""
    graph = nx.DiGraph()

    # create the graph
    for art in project_builder.builders:
        graph.add_node(art.name)

        for part in art.partof:
            graph.add_edge(part, art.name)

    for art in project_builder.builders:
        art.set_parts(set(graph.neighbors(art.name)))

    project_builder.set_graph(graph)


# pylint: disable=too-many-locals
def update_completion(project_builder):
    """Compute and update the completion values of all artifacts."""
    builder_map = project_builder.builder_map
    graph = project_builder.graph

    sorted_graph = nx.algorithms.dag.topological_sort(graph)
    sorted_graph = list(sorted_graph)

    specified = {}
    tested = {}

    for art_name in reversed(sorted_graph):
        builder = builder_map.get(art_name)
        stats = completion.impl_to_statistics(builder.impl, builder.subparts)
        (count_spc, value_spc, count_tst, value_tst) = stats

        if art_name.is_tst():
            for neighbor_name in graph.neighbors(art_name):
                value_spc += specified[neighbor_name]
                count_spc += 1
            value_tst = value_spc
            count_tst = count_spc
        else:
            for neighbor in graph.neighbors(art_name):
                value_tst += tested[neighbor]
                count_tst += 1

                if not neighbor.is_tst():
                    value_spc += specified[neighbor]
                    count_spc += 1

        specified[art_name] = utils.ratio(value_spc, count_spc)
        tested[art_name] = utils.ratio(value_tst, count_tst)

    for builder in project_builder.builders:
        comp = completion.Completion(
            spc=round(specified[builder.name], 3),
            tst=round(tested[builder.name], 3),
        )
        builder.set_completion(comp)
