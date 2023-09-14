import os
from singleton_decorator import singleton

from defi_llama_ews_app.services import logger
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.model.model_wirex_stablecoin import ModelWirexStableCoin
from defi_llama_ews_app.decorator.decorator_defi_llama_json_headers_required \
                                       import defi_llama_json_headers_required
from defi_llama_ews_app.converters.converter_dict_to_model_stablecoin import \
                                        ConverterDefiLlamaDictToModelStableCoin
from defi_llama_ews_app.service_interfaces.service_defi_llama_json_retriever_interface \
                                            import ServiceDefiLlamaJsonRetrieverInterface


@singleton
class ServiceDefiLlamaModelStablecoinRetriever(ServiceDefiLlamaJsonRetrieverInterface):
      
    @defi_llama_json_headers_required
    def __init__(self, defi_lama_json_headers) -> None:
        super().__init__()
        self._logger_instance     = logger
        self._headers             = defi_lama_json_headers
        self._converter           = ConverterDefiLlamaDictToModelStableCoin()
        self._url                 = 'https://defillama.com/stablecoins'
        self._peg_boundry         = os.environ.get('PEG_DEVIATION_ALERT', None)

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
    def url_json(self):
        return 'stablecoins.json'
    
    @property
    def intial_key(self):
        return 'pageProps'
    
    @property
    def second_key(self):
        return 'filteredPeggedAssets'
    
    def filter_results(self, stablecoins):
        currency_list = ModelWirexStableCoin.objects.values_list('currency', flat=True)
        wx_stables =  [x for x in stablecoins if x['symbol'] in currency_list and int(x['pegDeviation']) >= int(self._peg_boundry)] 
        return wx_stables

    def retrieve(self):
        jsons = super().retrieve()
        model_objects = []
        if jsons:
            for value in jsons:
                obj = self._converter.convert(
                                                trading_affected = True,
                                                dict             = value,
                                                url              = self._url,
                                                alert_priority   = EnumPriority.HIGH,
                                                alert_category   = EnumHighAlertWarningKeyWords.DEPEG)
                model_objects.append(obj)

        return model_objects