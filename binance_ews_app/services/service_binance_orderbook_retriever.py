from binance_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from ews_app.decorators.decorator_orderbook_urls_required import \
                                           orderbook_urls_required
from ews_app.decorators.decorator_wx_tickers_spot_list_required import \
                                                  wirex_spot_tickers_list
from ews_app.service_interfaces.service_orderbook_retriever_interface import \
                                            ServiceOrderBookRetrieverInterface


class ServiceBinanceOrderbookRetriever(ServiceOrderBookRetrieverInterface):

    @orderbook_urls_required
    @wirex_spot_tickers_list
    def __init__(self, 
                 binance_url, 
                 wx_tickers_spot_list_binance_format,
                 **kwargs) -> None:
        self._logger_instance       = logger
        self._binance_url           = binance_url
        self._raw_tickers_spot_list = wx_tickers_spot_list_binance_format

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def tickers_list(self) -> list[str]:
        return self._raw_tickers_spot_list
    
    @property
    def url(self) -> str:
        return self._binance_url
    
    @property
    def key_1(self) -> str:
        return None
    
    @property
    def symbol_key(self)-> str:
        return 'symbol'
    
    @property
    def time_key(self)-> str:
        return None
    
    @property
    def bid_price_key(self)-> str:
        return 'bidPrice'
    
    @property
    def bid_volume_key(self)-> str:
        return 'bidQty'
    
    @property
    def ask_price_key(self)-> str:
        return 'askPrice'
    
    @property
    def ask_volume_key(self)-> str:
        return 'askQty'

    @property
    def source(self):
        return EnumSource.BINANCE