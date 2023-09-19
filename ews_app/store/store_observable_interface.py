from typing import Dict, Mapping, TypeVar, Iterator

M = TypeVar('M')
E = TypeVar('E')

class StoreInterface(Mapping[E, M]):

    def __init__(self):
        self.d: Dict[E, M] = dict()

    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)

    def update_value(self, instance: M):
        if instance is None:
            return
        
        if not instance.symbol in self.d:
            self.d[instance.symbol].set_instance(instance)

    def get_value(self, instance: M):
        return self.d[instance.symbol]
    
    def remove_value(self, instance: M):
        if instance.symbol in self.d:
            del self.d[instance.symbol]
            
    def remove_value_by_key(self, key: E):
        if key in self.d:
            del self.d[key]       
