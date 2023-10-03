from abc import ABC
from typing import Dict, Iterator, Mapping, TypeVar


E=TypeVar('E')
M=TypeVar('M')

class ObserverInterface(ABC, Mapping[E, M]):
    """
    The Observer interface declares the update method, used by subjects.
    """

    def update(self, key: E, instance: M, old_instance: M, change: object) -> None:
        """
        Receive update from subject.
        """
        raise NotImplementedError(f"ObserverInterface: update not implemented for E: {str(E)} and M: {str(M)}")
    
    def update_many(self, instances = Dict[E, M], **kwargs) -> None:
        """
        Receive updates from subject.
        """
        raise NotImplementedError(f"ObserverInterface: update_many not implemented for E: {str(E)} and M: {str(M)}")
    
    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)