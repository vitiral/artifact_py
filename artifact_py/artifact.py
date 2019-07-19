from . import utils

class Artifact:
    def __init__(self, settings, name, file_, partof, section, subparts, done):
        self._settings = settings
        self.name = name
        self.file = file_
        self.partof = partof
        self.section = section
        self.subparts = subparts
        self.done = done

        # TODO: calculated
        # self.parts = parts
        # self.completed = completed
        # self.impl_ = impl

    def serialize(self):
        return {
            "name": self.name.serialize(),
            "file": self._settings.relpath(self.file),
            "partof": sorted(utils.serialize_list(self.partof)),
            "text": self.section.to_lines(),
            "subparts": sorted(self.subparts),
            "done": utils.serialize(self.done),

            # TODO: calculated
            # "parts": sorted(utils.serialize_all(self.parts)),
            # "completed": self.completed.serialize(),
            # "impl": self._impl.serialize(),
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
        return cls(
            name=name,
            file_=file_,
            section=section,
            partof=attributes.pop('partof', set()),
            subparts=attributes.pop('subparts', set()),
            done=attributes.pop('done', None),
            extra=attributes,
        )

    def set_parts(self, parts):
        self.parts = parts

    def build(self, settings):
        return Artifact(
            settings=settings,
            name=self.name,
            file_=self.file,
            partof=self.partof,
            subparts=self.subparts,
            section=self.section,
            done=self.done,
        )
