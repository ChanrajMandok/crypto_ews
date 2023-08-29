from datetime import datetime
from typing import Dict, TypeVar, Mapping, Iterator
from ews_app.observers.observer_interface import ObserverInterface

M = TypeVar('M')
E = TypeVar('E')


class StoreStaticObservableInterface(Mapping[E, M]):
    
    def __init__(self):
        self.__last_updated = None
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
        self.log_store_last_update()
        if key not in self.__data:
            self.__data[key] = instance
            self._notify_addition(key, instance)

    def remove(self, key: E) -> None:
        if key in self.__data:
            del self.__data[key]

    def exists(self, key: E) -> bool:
        return key in self.__data
    
    def log_store_last_update(self):
        now = int(datetime.now().timestamp())*1000
        self.__last_updated = now

    def get_last_updated_ts(self):
        return self.__last_updated

    def _notify_addition(self, key: E, instance: M) -> None:
        for observer in self.__observers:
            observer.update(key=key, instance=instance)

    def attach(self, observer: ObserverInterface) -> None:
        self.__observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self.__observers.remove(observer)