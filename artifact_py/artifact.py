
class Artifact:
    def __init__(self, name, file_, partof, parts, completed, text, impl_, subnames, done):
        self.name = name
        self.file = file_
        self.partof = partof
        self.parts = parts
        self.completed = completed
        self.text = text
        self.impl_ = impl
        self.subnames = subnames
        self.done = done


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
        return cls(
            name=dct['name'] if name is None else name,
            file_=dct['file'] if file_ is None else file_,
            partof=dct.get('partof', set()),
            subnames=dct.get('subnames', set()),
            done=dct.get('done'))
