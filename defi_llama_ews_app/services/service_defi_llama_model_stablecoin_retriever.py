import os

from singleton_decorator import singleton

from defi_llama_ews_app.services import logger
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.model.model_wirex_stablecoin import ModelWirexStableCoin
from defi_llama_ews_app.converters.converter_dict_to_model_stablecoin import \
                                       ConverterDefiLlamaDictToModelStableCoin
from defi_llama_ews_app.decorator.decorator_defi_llama_json_headers_required import \
                                                     defi_llama_json_headers_required
from defi_llama_ews_app.service_interfaces.service_defi_llama_json_retriever_interface import \
                                                         ServiceDefiLlamaJsonRetrieverInterface

@singleton
class ServiceDefiLlamaModelStablecoinRetriever(ServiceDefiLlamaJsonRetrieverInterface):
      
    @defi_llama_json_headers_required
    def __init__(self, defi_lama_json_headers) -> None:
        super().__init__()
        self._logger_instance     = logger
        self._headers             = defi_lama_json_headers
        self._converter           = ConverterDefiLlamaDictToModelStableCoin()
        self._url                 = 'https://defillama.com/stablecoins'
        self._peg_boundry         = os.environ.get('PEG_DEVIATION_ALERT', 1)

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
    
    def filter_results(self, object_list, test: bool = False):
        
        # Fetching currency list and handling potential exceptions
        try:
            currency_list = ModelWirexStableCoin.objects.values_list('currency', flat=True)
            if test:
                test_stables = [x for x in object_list if x['symbol'] in currency_list]
                return test_stables
        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: Failed to fetch currency list. Reason: {e}")
            return []

        peg_boundries = {
            'peggedUSD': float(self._peg_boundry),
            'peggedEUR': float(self._peg_boundry)+0.075
        }

        filtered_objects = []

        for x in object_list:
            if not isinstance(x, dict):  # Ensure each object is a dictionary
                continue

            if x.get('symbol') not in currency_list:
                continue

            pegType = x.get('pegType')
            price = x.get('price')

            # Check if necessary keys are present
            if not pegType or not price:
                self.logger_instance.error(f"{self.class_name} - ERROR: 'pegType' or 'price' key missing for symbol {x.get('symbol', 'UNKNOWN')}")
                continue

            # Ensure that price is a valid number
            try:
                price = float(price)
            except (ValueError, TypeError):
                self.logger_instance.error(f"{self.class_name} - ERROR: Invalid price value for symbol {x.get('symbol', 'UNKNOWN')}")
                continue

            peg_value = peg_boundries.get(pegType)
            
            # If pegType is not recognized
            if peg_value is None:
                self.logger_instance.error(f"{self.class_name} - ERROR: Unrecognized pegType '{pegType}' for symbol {x.get('symbol', 'UNKNOWN')}")
                continue

            try:
                peg_deviation = price - peg_value
            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: Failed to calculate peg deviation for symbol {x.get('symbol', 'UNKNOWN')}. Reason: {e}")
                continue

            if peg_deviation < -0.05 or peg_deviation > 0.05:
                filtered_objects.append(x)
        return filtered_objects

    def retrieve(self, test: bool= False):
        jsons = super().retrieve(test=test)
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