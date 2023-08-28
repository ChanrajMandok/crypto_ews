from datetime import datetime
from singleton_decorator import singleton

from binance_ews_app.store.stores_binance import \
                                     StoresBinance
from ews_app.observers.observer_interface import \
                                 ObserverInterface
from binance_ews_app.model.model_binance_event import \
                                      ModelBinanceEvent
from binance_ews_app.converters.converter_model_event_to_ms_teams_message \
                                 import ConverterModelEventToMsTeamsMessage


@singleton
class ObserverBinanceStoreEvent(ObserverInterface):
    
    def __init__(self) -> None:
        StoresBinance.store_binance_events.attach(self)
        self.converter_model_event_to_ms_teams_message = \
                      ConverterModelEventToMsTeamsMessage()
        
    def update(self, key: str, instance: ModelBinanceEvent):
      pass  
        # ts_now = int(datetime.now().timestamp())*1000
        # timestamps = instance.important_dates
        
        # ms_teams_messages = []

        # for timestamp in timestamps:
        #     if timestamp > ts_now:
        #         message = self.converter_model_event_to_ms_teams_message.convert(instance)
        #         print(message)

