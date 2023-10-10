from binance_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from binance_ews_app.decorators.decorator_binance_urls_required import \
                                                    binance_url_required
from ews_app.decorators.decorator_wx_tickers_spot_list_required import \
                                                 wirex_spot_tickers_list
from binance_ews_app.decorators.decorator_binance_headers_required import \
                                                   binance_headers_required
from ews_app.service_interfaces.service_delisting_retriever_interface import \
                                            ServiceDelistingRetrieverInterface


class ServiceBinanceDelistingRetriever(ServiceDelistingRetrieverInterface):

    @binance_url_required
    @wirex_spot_tickers_list
    @binance_headers_required
    def __init__(self, 
                 binance_delist_url,
                 binance_delist_headers, 
                 wx_tickers_spot_list_binance_format,
                 **kwargs) -> None:
        self._logger_instance       = logger
        self._binance_url           = binance_delist_url
        self._headers               = binance_delist_headers
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
    def headers(self):
        return self._headers
    
    @property
    def key_1(self) -> str:
        return 'data'
    
    @property
    def symbol_key(self) -> str:
        return 's'
        
    @property
    def expiry_key(self) -> str:
        return 'pomt'
    
    @property
    def source(self):
        return EnumSource.BINANCE