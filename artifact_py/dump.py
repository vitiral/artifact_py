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

    # remove trailing whitespace
    last_section = get_last_section(project)
    last_contents = None
    if last_section:
        last_contents = last_section.contents
        strip_endlines(last_contents)

    if last_contents is not None:
        last_contents.append(_empty_txt())

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
                reference_link(project.settings, artifact.name,
                               impl.primary[0]))

        subparts = sorted(six.iteritems(impl.secondary), key=lambda x: x[0])
        for subpart, codelocs in subparts:
            reference_links.append(
                reference_link(project.settings,
                               artifact.name,
                               codelocs[0],
                               subpart=subpart))

    if reference_links:
        reference_links.append(anchor_txt.Text([""]))

    get_last_section(project).contents.extend(reference_links)


def reference_link(settings, name, codeloc, subpart=None):
    if subpart is None:
        reference = name.raw
    else:
        reference = '{}.{}'.format(name.raw, subpart.raw)

    link = settings.code_url.format(
        file=settings.relpath(codeloc.file),
        line=codeloc.line,
    )
    return anchor_txt.ReferenceLink.from_parts(
        reference=reference,
        link=link,
    )


def get_last_section(project):
    last = None
    if project.sections:
        last = project.sections[-1]
    if last is None:
        return None
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


def _empty_txt():
    return anchor_txt.Text([""])


def _is_artifact_reference(content):
    return (isinstance(content, anchor_txt.ReferenceLink)
            and code.NAME_FULL_RE.match(content.reference))



def strip_endlines(contents):
    if not contents:
        return

    # gather the raw from all text objects
    texts = []
    for i in reversed(range(len(contents))):
        if isinstance(contents[i], anchor_txt.Text):
            texts.append(contents.pop(i))
        else:
            break

    texts.reverse()
    raw = []
    for t in texts:
        raw.extend(t.raw)

    for i in reversed(range(len(raw))):
        if raw[i] == "":
            raw.pop(i)
        else:
            break

    if raw:
        contents.append(anchor_txt.Text(raw))
