from typing import TypeVar, Iterator, Optional

M = TypeVar('M')
E = TypeVar('E')

class StoreInterface(dict[E, M]):

    def __init__(self):
        super().__init__()
        self.d: dict[E, M] = dict()

    def __getitem__(self, item: E) -> M:
        return self.d[item]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)

    def update_value(self, instance: Optional[M]):
        if instance is None:
            return
        key = getattr(instance, 'symbol', None)
        if key is not None:
            self.d[key] = instance

    def get_value(self, key: E) -> Optional[M]: 
        return self.d.get(key, None) 

    def remove_value(self, key: E):
        self.d.pop(key, None) 

    def remove_value_by_key(self, key: E):
        self.d.pop(key, None)
