from django.db import models
from datetime import datetime
from typing import Iterator, Optional, TypeVar, Mapping, Any

from token_risk_view_app.enum.enum_warning_price_change import \
                                          EnumWarningPriceChange
from ews_app.observer_interfaces.observer_interface import ObserverInterface

E = TypeVar('E', bound=str)
M = TypeVar('M', bound=models.Model)
G = TypeVar('G', bound=list[str])


class StoreTokenPriceChangeInterface(Mapping[E, M]):

    def __init__(self, update_increments: G) -> None:
        self.update_increments : G = update_increments
        self.data: dict[E, dict[E, Any]] = {
            update_increment: {"data": {}, "last_updated": None} for update_increment in self.update_increments }
        self.observers: list[ObserverInterface] = []
        self.accumulated_updates: list[tuple[E, E, Optional[M], Optional[M]]] = []

    def __getitem__(self, item: E) -> M:
        return self.data[item]["data"]

    def __len__(self) -> int:
        total = 0
        for update_increment in self.update_increments :
            total += len(self.data[update_increment]["data"])
        return total

    def __iter__(self) -> Iterator[E]:
        for update_increment in self.update_increments :
            yield from self.data[update_increment]["data"]

    def price_change_warning(self, old: Optional[M], new: M, update_increment: E) -> bool:
        if old is None:
            return False

        threshold = EnumWarningPriceChange.get(update_increment.upper()).value
        return abs((new - old) / old) > threshold

    def set_instance(self, update_increment: E, key: E, instance: M, batch_mode: bool = False) -> None:
        old_instance = self.data[update_increment]["data"].get(key)
        should_notify = self.price_change_warning(old=old_instance, new=instance, update_increment=update_increment)

        self.data[update_increment]["data"][key] = instance
        self.update_last_update_ts(update_increment=update_increment)

        if should_notify:
            if not batch_mode:
                self.notify(
                            update_increment=update_increment, 
                            key=key, 
                            instance=instance, 
                            old_instance=old_instance
                           )
            else:
                self.accumulated_updates.append((update_increment, key, instance, old_instance))

    def remove_instance(self, update_increment: E, key: E, batch_mode: bool = False) -> None:
        if key in self.data[update_increment]["data"]:
            old_instance = self.data[update_increment]["data"].pop(key)
            
            if not batch_mode:
                self.notify(
                            update_increment=update_increment, 
                            key=key, 
                            instance=None, 
                            old_instance=old_instance
                           )
            else:
                self.accumulated_updates.append((update_increment, key, None, old_instance))

    def update_last_update_ts(self, 
                              update_increment: E, 
                              timestamp: Optional[int] = None) -> None:
        
        if not timestamp or not isinstance(timestamp, int):
            timestamp = int(datetime.now().timestamp() *1000)
        
        self.data[update_increment]["last_updated"] = timestamp
        
    def get_last_updated_timestamps(self) -> dict[E, Optional[int]]:
        return {update_increment: details["last_updated"] for update_increment, details in self.data.items()}

    def attach(self, observer: ObserverInterface) -> None:
        self.observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self.observers.remove(observer)

    def notify(self, update_increment: E, key: E, instance: Optional[M], old_instance: Optional[M]) -> None:
        for observer in self.observers:
            observer.update(
                update_increment=update_increment, 
                key=key, 
                instance=instance, 
                old_instance=old_instance
            )

    def batch_update(self, orderbooks: dict[E, M], update_increments: G) -> None:
        for update_increment in update_increments:
            for key, instance in orderbooks.items():
                self.set_instance(
                    update_increment=update_increment,
                    key=key,
                    instance=instance,
                    batch_mode=True
                )

        self.send_batch_notifications()

    def send_batch_notifications(self) -> None:
        for update_increment, key, instance, old_instance in self.accumulated_updates:
            self.notify(
                        update_increment=update_increment, 
                        key=key, 
                        instance=instance, 
                        old_instance=old_instance
                        )
        self.accumulated_updates.clear()