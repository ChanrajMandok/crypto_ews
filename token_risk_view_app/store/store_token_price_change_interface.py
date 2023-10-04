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
    
    """
    A class to store and manage token price changes, and notify observers of significant price changes.

    Implements the Observer design pattern where this class is the subject.
    This class also implements the Mapping protocol to behave like a dictionary.
    """

    def __init__(self, update_increments: G) -> None:
        self.update_increments: G = update_increments
        self.data: dict[E, dict[E, Any]] = {
            update_increment: {"data": {}, "last_updated": None} for update_increment in self.update_increments}
        self.observers: list[ObserverInterface] = []
        self.accumulated_updates: list[tuple[E, E, Optional[M], Optional[M]]] = []

    def __getitem__(self, item: E) -> M:
        """Retrieve token price data for a given key."""
        
        return self.data[item]["data"]

    def __len__(self) -> int:
        """Return the total number of token price data across all update increments."""
        
        total = 0
        total = 0
        for update_increment in self.update_increments:
            total += len(self.data[update_increment]["data"])
        return total

    def __iter__(self) -> Iterator[E]:
        """Iterate over token price data keys across all update increments."""
        for update_increment in self.update_increments:
            yield from self.data[update_increment]["data"]

    def price_change_warning(self, old: Optional[M], new: M, update_increment: E) -> bool:
        """
        Check if the price change between the old and new instances exceeds the threshold.
        """
        
        if old is None:
            return False

        threshold = EnumWarningPriceChange[update_increment].value
        return abs((new.bid.price - old.bid.price) / old.bid.price) > threshold

    def set_instance(self, update_increment: E, key: E, instance: M) -> None:
        """
        Set (or update) an instance of token price data for a given key and update increment.

        This method will also check if the price change warning should be triggered and if so,
        accumulates the update to notify the observers later.
        """
        
        self.update_last_update_ts(update_increment=update_increment)
        old_instance = self.data[update_increment]["data"].get(key)
        should_notify = self.price_change_warning(old=old_instance, new=instance, update_increment=update_increment)

        self.data[update_increment]["data"][key] = instance

        if should_notify:
            self.accumulated_updates.append((update_increment, key, instance, old_instance))
            self.notify()

    def set_instances(self, update_increments: G, orderbooks: dict[E, M]) -> None:
        """
        Set (or update) multiple instances of token price data.

        This method will check for each instance whether the price change warning should be triggered,
        and if so, accumulates those updates. At the end, it will notify the observers with all accumulated updates.
        """
        
        for update_increment in update_increments:    
            self.update_last_update_ts(update_increment=update_increment)
            for key, instance in orderbooks.items():
                old_instance = self.data[update_increment]["data"].get(key)
                should_notify = self.price_change_warning(old=old_instance, new=instance, update_increment=update_increment)

                self.data[update_increment]["data"][key] = instance

                if should_notify:
                    self.accumulated_updates.append((update_increment, key, instance, old_instance))

        # Once all instances are set for the given update_increments, notify observer with accumulated updates
        if len(self.accumulated_updates) > 0:
            self.notify()

    def remove_instance(self, update_increment: E, key: E) -> None:
        """
        Remove an instance of token price data for a given key and update increment.
        The removed instance is accumulated to notify the observers.
        """
        
        if key in self.data[update_increment]["data"]:
            old_instance = self.data[update_increment]["data"].pop(key)
            self.accumulated_updates.append((update_increment, key, None, old_instance))
            self.notify()

    def update_last_update_ts(self, update_increment: E, timestamp: Optional[int] = None) -> None:
        """
        Update the last updated timestamp for a given update increment.

        If no timestamp is provided or the given timestamp isn't of type int, the current timestamp is used.
        """
        
        if not timestamp or not isinstance(timestamp, int):
            timestamp = int(datetime.now().timestamp() * 1000)
        self.data[update_increment]["last_updated"] = timestamp

    def get_last_updated_timestamps(self) -> dict[E, Optional[int]]:
        """
        Retrieve the last updated timestamps for all update increments.
        """
        
        return {update_increment: details["last_updated"] for update_increment, details in self.data.items()}

    def attach(self, observer: ObserverInterface) -> None:
        """
        Attach an observer from being notified of changes.
        """

        self.observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        """
        Detach an observer from being notified of changes.
        """
        self.observers.remove(observer)

    def notify(self) -> None:
        """
        Notify all attached observers of the accumulated updates.
        After notifying all observers, the accumulated updates are cleared.
        """
        
        for observer in self.observers:
            observer.update(self.accumulated_updates)
        self.accumulated_updates.clear()
