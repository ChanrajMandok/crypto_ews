from typing import Dict, Iterator, Mapping, TypeVar

from ews_app.observers.observer_interface import ObserverInterface

M = TypeVar('M')
E = TypeVar('E')


class StoreObservableInterface(Mapping[E, M]):

    def __init__(self):
        self.d: Dict[str, M] = dict()
        self.observers = []

    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)
    
    def set_instance(self, key: E, instance: M, old_instance: M = None, change: object = None) -> None:
        self.d[str(key)] = instance
        self.notify(key=key, instance=instance, old_instance=old_instance, change=change)
        
    def set_instances(self, instances: Dict[E, M], **kwargs) -> None:
        for key in instances:
            self.d[key] = instances[key]
        loop = kwargs["loop"] if "loop" in kwargs else None
        self.notify_many(instances=instances, loop=loop)

    def remove_instances(self, instances: Dict[E, M]) -> None:
        for key in instances:
            del self.d[key]
        self.notify_many(instances=instances)
        
    def remove_instance(self, key: E) -> M:
        instance = self.d[str(key)]
        del self.d[key]
        self.notify(key, instance = None, old_instance = instance)
        return instance
    
    def attach(self, observer: ObserverInterface) -> None:
        self.observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self.observers.remove(observer)

    def notify(self, key: E, instance: M, old_instance: M, change: object = None) -> None:
        for observer in self.observers:
            observer.update(key=key, instance=instance, old_instance=old_instance, change=change)
            
    def notify_many(self, instances: Dict[E, M], **kwargs) -> None:
        loop = kwargs["loop"] if "loop" in kwargs else None
        for observer in self.observers:
            observer.update_many(instances=instances, loop=loop)
