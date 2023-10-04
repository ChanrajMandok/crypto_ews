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
        self.update_increments: G = update_increments
        self.data: dict[E, dict[E, Any]] = {
            update_increment: {"data": {}, "last_updated": None} for update_increment in self.update_increments}
        self.observers: list[ObserverInterface] = []
        self.accumulated_updates: list[tuple[E, E, Optional[M], Optional[M]]] = []

    def __getitem__(self, item: E) -> M:
        return self.data[item]["data"]

    def __len__(self) -> int:
        total = 0
        for update_increment in self.update_increments:
            total += len(self.data[update_increment]["data"])
        return total

    def __iter__(self) -> Iterator[E]:
        for update_increment in self.update_increments:
            yield from self.data[update_increment]["data"]

    def price_change_warning(self, old: Optional[M], new: M, update_increment: E) -> bool:
        if old is None:
            return False

        threshold = EnumWarningPriceChange[update_increment].value
        return abs((new.bid.price - old.bid.price) / old.bid.price) > threshold

    def set_instance(self, update_increment: E, key: E, instance: M) -> None:
        self.update_last_update_ts(update_increment=update_increment)
        old_instance = self.data[update_increment]["data"].get(key)
        should_notify = self.price_change_warning(old=old_instance, new=instance, update_increment=update_increment)

        self.data[update_increment]["data"][key] = instance

        if should_notify:
            self.accumulated_updates.append((update_increment, key, instance, old_instance))
            self.notify()

    def set_instances(self, update_increments: G, orderbooks: dict[E, M]) -> None:
        for update_increment in update_increments:    
            self.update_last_update_ts(update_increment=update_increment)
            for key, instance in orderbooks.items():
                old_instance = self.data[update_increment]["data"].get(key)
                should_notify = self.price_change_warning(old=old_instance, new=instance, update_increment=update_increment)

                self.data[update_increment]["data"][key] = instance

                if should_notify:
                    self.accumulated_updates.append((update_increment, key, instance, old_instance))

        # Once all instances are set for the given update_increments, notify observer with accumulated updates
        self.notify()

    def remove_instance(self, update_increment: E, key: E) -> None:
        if key in self.data[update_increment]["data"]:
            old_instance = self.data[update_increment]["data"].pop(key)
            self.accumulated_updates.append((update_increment, key, None, old_instance))
            self.notify()

    def update_last_update_ts(self, update_increment: E, timestamp: Optional[int] = None) -> None:
        if not timestamp or not isinstance(timestamp, int):
            timestamp = int(datetime.now().timestamp() * 1000)
        self.data[update_increment]["last_updated"] = timestamp

    def get_last_updated_timestamps(self) -> dict[E, Optional[int]]:
        return {update_increment: details["last_updated"] for update_increment, details in self.data.items()}

    def attach(self, observer: ObserverInterface) -> None:
        self.observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self.accumulated_updates)
        self.accumulated_updates.clear()
