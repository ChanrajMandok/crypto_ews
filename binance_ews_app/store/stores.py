from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from ews_app.store.store_observable_interface import StoreObservableInterface


class StoresBinance:

    store_binance_events = StoreObservableInterface[str, ModelBinanceEvent]()