from okx_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from okx_ews_app.decorator.decorator_okx_headers_required import \
                                              okx_headers_required
from ews_app.decorators.decorator_wx_tickers_spot_list_required import \
                                                 wirex_spot_tickers_list
from okx_ews_app.decorator.decorator_okx_urls_required import okx_url_required
from ews_app.service_interfaces.service_delisting_retriever_interface import \
                                            ServiceDelistingRetrieverInterface


class ServiceOkxDelistingRetriever(ServiceDelistingRetrieverInterface):

    @okx_url_required
    @okx_headers_required
    @wirex_spot_tickers_list
    def __init__(self, 
                 okx_headers, 
                 okx_delist_url,
                 wx_tickers_spot_list_okx_format,
                 **kwargs) -> None:
        self._logger_instance       = logger
        self._headers               = okx_headers
        self._okx_url               = okx_delist_url
        self._raw_tickers_spot_list = wx_tickers_spot_list_okx_format

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
        return self._okx_url

    @property
    def headers(self):
        return self._headers
    
    @property
    def key_1(self) -> str:
        return 'data'
    
    @property
    def symbol_key(self) -> str:
        return 'instId'
        
    @property
    def expiry_key(self) -> str:
        return 'expTime'
    
    @property
    def source(self):
        return EnumSource.OKX