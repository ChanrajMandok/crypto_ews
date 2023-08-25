from singleton_decorator import singleton

from binance_ews_app.store.stores_binance import StoresBinance
from ews_app.observers.observer_interface import ObserverInterface
from binance_ews_app.model.model_binance_event import ModelBinanceEvent


@singleton
class ObserverBinanceStoreEvent(ObserverInterface):
    
    def __init__(self) -> None:
        StoresBinance.store_binance_events.attach(self)
        
    def udpate(self, key: str, instance: ModelBinanceEvent):
        
        print(key)
        
        
        