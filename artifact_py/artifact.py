class Artifact:
    def __init__(self, settings, name, file_, partof, section, subnames, done):
        self._settings = settings
        self.name = name
        self.file = file_
        self.partof = partof
        self.section = section
        self.subnames = subnames
        self.done = done

        # TODO: calculated
        # self.parts = parts
        # self.completed = completed
        # self.impl_ = impl

    def serialize(self):
        return {
            "name": self.name.serialize(),
            "file": self.file,  # TODO: remove root
            "partof": sorted(utils.serialize_all(self.partof)),
            "text": self.section.to_lines(),
            "subnames": sorted(utils.serialize_all(self.subnames)),
            "done": self.done.serialize(),

            # TODO: calculated
            # "parts": sorted(utils.serialize_all(self.parts)),
            # "completed": self.completed.serialize(),
            # "impl": self._impl.serialize(),
        }


class ArtifactBuilder:
    """Intermediate artifact."""
    def __init__(self, name, file_, section, partof, subnames, done, extra):
        self.name = name
        self.file = file_
        self.section = section
        self.partof = partof
        self.subnames = subnames
        self.done = done
        self.extra = extra

        self.parts = {}
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
            subnames=attributes.pop('subnames', set()),
            done=attributes.pop('done', None),
            extra=attributes,
        )

    def build(self, settings):
        return Artifact(
            settings=settings,
            name=self.name,
            file_=self.file,
            partof=self.partof,
            subnames=self.subnames,
            section=self.section,
            done=self.done,
        )
