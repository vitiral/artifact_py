class Artifact:
    def __init__(self, settings, name, file_, partof, parts, completed,
                 section, impl_, subnames, done):
        self._settings = settings
        self.name = name
        self.file = file_
        self.partof = partof
        self.parts = parts
        self.completed = completed
        self.section = section
        self.impl_ = impl
        self.subnames = subnames
        self.done = done

    def serialize(self):
        return {
            "name": self.name.serialize(),
            "file": self.file,  # TODO: remove root
            "partof": sorted(utils.serialize_all(self.partof)),
            "parts": sorted(utils.serialize_all(self.parts)),
            "completed": self.completed.serialize(),
            "text": self.text,
            "impl": self._impl.serialize(),
            "subnames": sorted(utils.serialize_all(self.subnames)),
            "done": self.done.serialize(),
        }


class ArtifactIm:
    """Intermediate artifact."""
    def __init__(self, name, file_, partof, subnames, done):
        self.name = name
        self.file = file_
        self.partof = partof
        self.subnames = subnames
        self.done = done

    @classmethod
    def from_dict(cls, dct, name=None, file_=None):
        """Construct from a dictionary, with some overloads available."""
        return cls(name=dct['name'] if name is None else name,
                   file_=dct['file'] if file_ is None else file_,
                   partof=dct.get('partof', set()),
                   subnames=dct.get('subnames', set()),
                   done=dct.get('done'))
