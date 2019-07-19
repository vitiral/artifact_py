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
import copy

import six
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
    artifacts_builder = load_artifacts_builder(project_sections)
    return project.Project(
        settings=p_settings,
        artifacts=[b.build(p_settings) for b in artifacts_builder.builders],
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


def load_artifacts_builder(project_sections):
    graph = nx.DiGraph()

    builders = [
        s for s in project_sections if isinstance(s, artifact.ArtifactBuilder)
    ]

    # create the graph
    for art in builders:
        graph.add_node(art.name)

        for part in art.partof:
            graph.add_edge(part, art.name)

    for art in builders:
        art.set_parts(set(graph.neighbors(art.name)))

    return artifact.ArtifactsBuilder(builders=builders, graph=graph)


def determine_completed(artifacts_builder, impls):
    pass
    # // If there is a cycle we just return everything as 0% complete for spc+tst
    # // We ignore `done` because there will be an ERROR lint later anyway.
    # let uncomputed = || {
    #     impls
    #         .keys()
    #         .map(|n| (n.clone(), Completed::default()))
    #         .collect()
    # };
    # let sorted_graph = match petgraph::algo::toposort(&graphs.full, None) {
    #     Ok(s) => s,
    #     // cycle detected
    #     Err(_) => return uncomputed(),
    # };

    # // convert to by-id
    # let impls: IndexMap<GraphId, &_> = impls
    #     .iter()
    #     .map(|(name, v)| (graphs.lookup_id[name], v))
    #     .collect();

    # /// compute ratio but ignore count=0
    # fn ratio(value: f64, count: usize) -> f64 {
    #     if count == 0 {
    #         0.0
    #     } else {
    #         value / count as f64
    #     }
    # }

    # let mut implemented: IndexMap<GraphId, f64> = IndexMap::with_capacity(impls.len());
    # let mut tested: IndexMap<GraphId, f64> = IndexMap::with_capacity(impls.len());

    # for id in sorted_graph.iter().rev() {
    #     let name = expect!(graphs.lookup_name.get(id));
    #     let sub = match subnames.get(name) {
    #         Some(s) => s,
    #         None => continue, // Will cause warning lint error.
    #     };
    #     let impl_ = expect!(impls.get(id));
    #     let (mut count_spc, mut value_spc, mut count_tst, mut value_tst) = impl_.to_statistics(sub);

    #     if matches!(graphs.lookup_name[id].ty, Type::TST) {
    #         for part_id in graphs.full.neighbors(*id) {
    #             value_spc += implemented[&part_id];
    #             count_spc += 1;
    #         }
    #         value_tst = value_spc;
    #         count_tst = count_spc;
    #     } else {
    #         for part_id in graphs.full.neighbors(*id) {
    #             value_tst += tested[&part_id];
    #             count_tst += 1;

    #             if !matches!(graphs.lookup_name[&part_id].ty, Type::TST) {
    #                 // TST's dont contribute towards spc in other types
    #                 value_spc += implemented[&part_id];
    #                 count_spc += 1;
    #             }
    #         }
    #     }
    #     tested.insert(*id, ratio(value_tst, count_tst));
    #     implemented.insert(*id, ratio(value_spc, count_spc));
    # }

    # debug_assert_eq!(impls.len(), implemented.len());
    # debug_assert_eq!(impls.len(), tested.len());
    # let out: IndexMap<Name, Completed> = implemented
    #     .iter()
    #     .map(|(id, spc)| {
    #         // throw away digits after 1000 significant digit
    #         // (note: only at end of all calculations!)
    #         let compl = Completed {
    #             spc: round_ratio(*spc),
    #             tst: round_ratio(tested[id]),
    #         };
    #         (graphs.lookup_name[id].clone(), compl)
    #     })
    #     .collect();
    # debug_assert_eq!(impls.len(), out.len());
    # out
