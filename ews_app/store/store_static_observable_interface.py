from typing import Dict, TypeVar, Mapping, Iterator
from ews_app.observers.observer_interface import ObserverInterface

M = TypeVar('M')
E = TypeVar('E')


class StoreStaticObservableInterface(Mapping[E, M]):
    
    def __init__(self):
        self.__data: Dict[E, M] = {}
        self.__observers: list[ObserverInterface] = []
        
    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.__data[value]

    def __len__(self) -> int:
        return len(self.__data)

    def __iter__(self) -> Iterator[E]:
        return iter(self.__data)

    def add(self, key: E, instance: M) -> None:
        if key not in self.__data:
            self.__data[key] = instance
            self._notify_addition(key, instance)

    def remove(self, key: E) -> None:
        if key in self.__data:
            del self.__data[key]

    def exists(self, key: E) -> bool:
        return key in self.__data

    def _notify_addition(self, key: E, instance: M) -> None:
        for observer in self.__observers:
            observer.update(key=key, instance=instance)

    def attach(self, observer: ObserverInterface) -> None:
        self.__observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self.__observers.remove(observer)