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
from .name import SubPart
from . import completion


class Artifact:
    """Represents a design object which can be linked to other design objects.

    See #SPC-design.artifact
    """
    def __init__(
            self,
            name,
            file_,
            partof,
            subparts,
            impl,
            done,
            parts,
            completion,
            extra,
    ):
        self.name = name
        self.file = file_
        self.partof = partof
        self.subparts = subparts
        self.impl = impl
        self.done = done
        self.parts = parts
        self.completion = completion
        self.extra = extra

    def serialize(self, settings):
        return {
            "name": self.name.serialize(settings),
            "file": settings.relpath(self.file),
            "partof": sorted(settings.serialize_list(self.partof)),
            "subparts": sorted(settings.serialize_list(self.subparts)),
            "done": settings.serialize_maybe(self.done),
            "parts": sorted(settings.serialize_list(self.parts)),
            "impl": settings.serialize_maybe(self.impl),
            "completion": self.completion.serialize(settings),
            "extra": self.extra,
        }


class ArtifactBuilder:
    """Builder object for the artifact."""
    def __init__(self, name, file_, partof, subparts, done, extra):
        self.name = name
        self.file = file_
        self.partof = partof
        self.subparts = subparts
        self.done = done
        self.extra = extra

        self.impl = None
        self.parts = None
        self.completion = None

    @classmethod
    def from_attributes(cls, attributes, name, file_):
        """Construct from a dictionary, with some overloads available."""
        return cls.from_attributes_consume(attributes=dict(attributes),
                                           name=name,
                                           file_=file_)

    @classmethod
    def from_attributes_consume(cls, attributes, name, file_):
        name_raw = name.raw
        partof = utils.ensure_list(name_raw + ' partof',
                                   attributes.pop('partof', []))
        partof = {Name.from_str(n) for n in partof}

        subparts = utils.ensure_list(name_raw + ' subparts',
                                     attributes.pop('subparts', []))
        subparts = {SubPart.from_str(s) for s in subparts}
        done = utils.ensure_str(name_raw + ' done',
                                attributes.pop('done', None),
                                allow_none=True)

        attributes.pop('artifact', None)  # Normal settings. Ignore.
        return cls(
            name=name,
            file_=file_,
            partof=partof,
            subparts=subparts,
            done=done,
            extra=attributes,
        )

    def set_impl(self, impl):
        self.impl = impl

    def set_parts(self, parts):
        self.parts = parts

    def set_completion(self, completion):
        self.completion = completion

    def build(self):
        assert self.parts is not None, "must set_parts"
        assert self.completion is not None, "must set_completion"

        return Artifact(
            name=self.name,
            file_=self.file,
            partof=self.partof,
            subparts=self.subparts,
            impl=self.impl,
            done=self.done,
            parts=self.parts,
            completion=self.completion,
            extra=self.extra,
        )

    def __repr__(self):
        return "ArtifactBuilder({}, partof={})".format(self.name, self.partof)
