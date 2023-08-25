from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from ews_app.store.store_static_observable_interface import StoreStaticObservableInterface


class StoresBinance:

    store_binance_events =  StoreStaticObservableInterface[str, ModelBinanceEvent]()