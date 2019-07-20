import os
import copy
import re

import anchor_txt
import six

from . import code
from . import artifact


def dump_project(project, with_links=True):
    """Dump the artifact project with fresh reference links."""
    # make a copy so we can mutate things
    project = copy.deepcopy(project)

    # scrub all sections of things like reference links
    scrub_sections_recurse(project.sections)

    if with_links:
        # add our own references at the end
        update_reference_links(project)

    return project.to_lines()


def update_reference_links(project):
    if project.settings.code_url is None:
        return

    reference_links = []

    for artifact in project.artifacts:
        impl = artifact.impl
        if impl.primary:
            reference_links.append(
                format_reference_link(settings, artifact.name,
                                      impl.primary[0]))

        for subpart, codelocs in six.iteritems(impl.secondary):
            reference_links.append(
                reference_link(settings,
                               artifact.name,
                               codelocs[0],
                               subpart=subpart))

    last_section(project).contents.extend(reference_links)


def reference_link(settings, name, codeloc, subpart=None):
    if subpart is None:
        reference = name.raw
    else:
        reference = '{}.{}'.format(name.raw, subpart.raw)

    link = settings.code_loc.format(file=codeloc.file, line=codeloc.line)
    return anchor_txt.ReferenceLink.from_parts(
        reference=reference,
        link=link,
    )


def last_section(project):
    last = None
    if project.sections:
        last = project.sections[-1]
    assert last, "some section has to exist"
    return _last_section_recurse(last)


def _last_section_recurse(section):
    if isinstance(section, artifact.Artifact):
        section = section.section
    if section.sections:
        return _last_section_recurse(section.sections[-1])
    return section


def scrub_sections_recurse(sections):
    for section in sections:
        if isinstance(section, artifact.Artifact):
            section = section.section
        section.contents = [
            c for c in section.contents if not _is_artifact_reference(c)
        ]
        scrub_sections_recurse(section.sections)


def _is_artifact_reference(content):
    return (isinstance(content, anchor_txt.ReferenceLink)
            and code.NAME_CODE_VALID_RE.match(content.reference))
