from defi_llama_ews_app.services import logger
from ews_app.model.model_wirex_stablecoin import ModelWirexStableCoin
from defi_llama_ews_app.decorator.decorator_defi_llama_urls_required import \
                                                      defi_llama_urls_required
from defi_llama_ews_app.decorator.decorator_defi_llama_json_headers_required \
                                        import defi_llama_json_headers_required
from defi_llama_ews_app.service_interfaces.service_defi_llama_json_retriever_interface \
                                            import ServiceDefiLlamaJsonRetrieverInterface



class ServiceDefiLlamaBridgeHackRetriever(ServiceDefiLlamaJsonRetrieverInterface):
      
    @defi_llama_urls_required
    @defi_llama_json_headers_required
    def __init__(self,
                defi_lama_json_headers,
                defi_lama_bridge_hacks,
                defi_lama_base_url       = None,
                defi_lama_hacks_url      = None,
                defi_lama_stablecoin_url = None) -> None:
        super().__init__()
        self._logger_instance     = logger
        self._headers             = defi_lama_json_headers
        self._url                 = defi_lama_bridge_hacks

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def url_headers(self):
        return self._headers
    
    @property
    def url(self):
        return self._url
    
    @property
    def intial_key(self):
        return 'pageProps'