import six

from . import utils
from .name import Name
from . import completion


class Artifact:
    def __init__(self, settings, name, file_, partof, section, subparts, done, parts):
        self.name = name
        self.file = file_
        self.partof = partof
        self.section = section
        self.subparts = subparts
        self.done = done
        self.parts = parts

        # TODO: calculated
        # self.completed = completed
        # self.impl_ = impl

    def serialize(self, settings):
        return {
            "name": self.name.serialize(settings),
            "file": settings.relpath(self.file),
            "partof": sorted(settings.serialize_list(self.partof)),
            "text": self.section.to_lines(),
            "subparts": sorted(settings.serialize_list(self.subparts)),
            "done": settings.serialize_maybe(self.done),
            "parts": sorted(settings.serialize_list(self.parts)),

            # TODO: calculated
            # "completed": self.completed.serialize(settings),
            # "impl": self._impl.serialize(settings),
        }


class ArtifactBuilder:
    """Intermediate artifact."""
    def __init__(self, name, file_, section, partof, subparts, done, extra):
        self.name = name
        self.file = file_
        self.section = section
        self.partof = partof
        self.subparts = subparts
        self.done = done
        self.extra = extra

        self.parts = None
        self.completed = None
        self.impl = None

    @classmethod
    def from_attributes(cls, attributes, name, file_, section):
        """Construct from a dictionary, with some overloads available."""
        return cls.from_attributes_consume(attributes=dict(attributes),
                                           name=name,
                                           file_=file_,
                                           section=section)

    @classmethod
    def from_attributes_consume(cls, attributes, name, file_, section):
        partof = {Name.from_str(n) for n in attributes.pop('partof', [])}
        subparts = {
            completion.SubPart.from_str(s)
            for s in attributes.pop('subparts', [])
        }
        return cls(
            name=name,
            file_=file_,
            section=section,
            partof=partof,
            subparts=subparts,
            done=attributes.pop('done', None),
            extra=attributes,
        )

    def set_parts(self, parts):
        self.parts = parts

    def build(self, settings):
        assert self.parts is not None, "must set_parts"

        return Artifact(
            settings=settings,
            name=self.name,
            file_=self.file,
            partof=self.partof,
            subparts=self.subparts,
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
