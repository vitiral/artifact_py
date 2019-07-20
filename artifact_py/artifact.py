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
import six

from . import utils
from .name import Name
from . import completion


class Artifact:
    def __init__(
            self,
            name,
            file_,
            partof,
            section,
            subparts,
            impl,
            done,
            parts,
    ):
        self.name = name
        self.file = file_
        self.partof = partof
        self.section = section
        self.subparts = subparts
        self.impl = impl
        self.done = done
        self.parts = parts

        # TODO: calculated
        # self.completed = completed

    def serialize(self, settings):
        return {
            "name": self.name.serialize(settings),
            "file": settings.relpath(self.file),
            "partof": sorted(settings.serialize_list(self.partof)),
            "text": self.section.to_lines(),
            "subparts": sorted(settings.serialize_list(self.subparts)),
            "done": settings.serialize_maybe(self.done),
            "parts": sorted(settings.serialize_list(self.parts)),
            "impl": self.impl.serialize(settings),

            # TODO: calculated
            # "completed": self.completed.serialize(settings),
        }


class ArtifactBuilder:
    """Intermediate artifact."""
    def __init__(self, name, file_, impl, section, partof, subparts, done,
                 extra):
        self.name = name
        self.file = file_
        self.impl = impl
        self.section = section
        self.partof = partof
        self.subparts = subparts
        self.done = done
        self.extra = extra

        self.parts = None
        self.completed = None

    @classmethod
    def from_attributes(cls, attributes, name, file_, impl, section):
        """Construct from a dictionary, with some overloads available."""
        return cls.from_attributes_consume(attributes=dict(attributes),
                                           name=name,
                                           file_=file_,
                                           impl=impl,
                                           section=section)

    @classmethod
    def from_attributes_consume(cls, attributes, name, file_, impl, section):
        partof = {Name.from_str(n) for n in attributes.pop('partof', [])}
        subparts = {
            completion.SubPart.from_str(s)
            for s in attributes.pop('subparts', [])
        }
        return cls(
            name=name,
            file_=file_,
            impl=impl,
            section=section,
            partof=partof,
            subparts=subparts,
            done=attributes.pop('done', None),
            extra=attributes,
        )

    def set_parts(self, parts):
        self.parts = parts

    def build(self):
        assert self.parts is not None, "must set_parts"

        return Artifact(
            name=self.name,
            file_=self.file,
            partof=self.partof,
            subparts=self.subparts,
            impl=self.impl,
            section=self.section,
            done=self.done,
            parts=self.parts,
        )

    def __repr__(self):
        return "ArtifactBuilder({}, partof={})".format(self.name, self.partof)


class ArtifactsBuilder:
    def __init__(self, builders, graph):
        self.builders = builders
        self.graph = graph
