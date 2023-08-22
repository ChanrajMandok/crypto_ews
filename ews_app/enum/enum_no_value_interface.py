from enum import Enum


class NoValue(Enum):

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)