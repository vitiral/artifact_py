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
"""Dump data to a string or file."""
import copy
import re

import anchor_txt
import six

from . import code
from . import artifact

NAME_REFERENCE_STR = '@?' + code.NAME_FULL_STR
NAME_REFERENCE_RE = re.compile(NAME_REFERENCE_STR, re.I)


def dump_project(project, with_links=True):
    """Dump the artifact project with fresh reference links."""
    # make a copy so we can mutate things
    project = copy.deepcopy(project)

    # scrub all sections of things like reference links
    scrub_sections_recurse(project.root_section)

    lines = project.root_section.to_lines()
    strip_empty_lines(lines)

    if with_links:
        # add our own references at the end
        links = get_reference_links(project)
        if lines or links:
            lines.append('')
        lines.extend(links)

    return lines


def strip_empty_lines(lines):
    for i in reversed(range(len(lines))):
        if not lines[i].strip():
            lines.pop(i)
        else:
            break


def get_reference_links(project):
    """Return a project's reference links in markdown format."""
    if project.settings.code_url is None:
        return []

    reference_links = []

    for art in project.artifacts:
        name = art.name
        reference_links.append(reference_link_inline(name))
        for subpart in art.subparts:
            reference_links.append(reference_link_inline(name,
                                                         subpart=subpart))

    for name, impl in six.iteritems(project.impls):
        if impl.primary:
            reference_links.append(
                reference_link_code(project.settings, name, impl.primary[0]))

        subparts = sorted(six.iteritems(impl.secondary), key=lambda x: x[0])
        for subpart, codelocs in subparts:
            reference_links.append(
                reference_link_code(project.settings,
                                    name,
                                    codelocs[0],
                                    subpart=subpart))

    lines = []

    for reflink in reference_links:
        lines.extend(reflink.to_lines())

    lines.sort()

    if lines:
        lines.append('')

    return lines


def reference_link_inline(name, subpart=None):
    reference = reference_str(name, subpart)

    return anchor_txt.ReferenceLink.from_parts(
        reference=reference,
        link='#' + reference,
    )


def reference_link_code(settings, name, codeloc, subpart=None):
    reference = reference_str(name, subpart)

    link = settings.code_url.format(
        file=settings.relpath(codeloc.file),
        line=codeloc.line + 1,
    )
    return anchor_txt.ReferenceLink.from_parts(
        reference='@' + reference,
        link=link,
    )


def reference_str(name, subpart=None):
    if subpart is None:
        return name.raw
    return '{}.{}'.format(name.raw, subpart.raw)


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


def scrub_sections_recurse(section):
    section.contents = [
        c for c in section.contents if not _is_artifact_reference(c)
    ]

    for child in section.sections:
        scrub_sections_recurse(child)


def _is_artifact_reference(content):
    return (isinstance(content, anchor_txt.ReferenceLink)
            and NAME_REFERENCE_RE.match(content.reference))
