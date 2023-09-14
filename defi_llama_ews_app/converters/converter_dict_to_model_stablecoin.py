from defi_llama_ews_app.converters import logger
from defi_llama_ews_app.model.model_defi_stablecoin import ModelDefiStablecoin
from ews_app.converter_interfaces.converter_dict_to_model_stablecoin_interface \
                                   import ConverterDictToModelStablecoinInterface


class ConverterDefiLlamaDictToModelStableCoin(ConverterDictToModelStablecoinInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance = logger
        self._model_stable    = ModelDefiStablecoin
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property    
    def price_key(self) -> str:
        return 'price'

    @property
    def mechanism_key(self) -> str:
        return 'pegMechanism'
        
    @property
    def stablecoin_key(self) -> str:
        return 'symbol'
        
    @property
    def one_day_price_change_key(self) -> str:
        return 'change_1d'

    @property
    def peg_deviation_key(self) -> str:
        return 'pegDeviation'

    def model_stablecoin(self):
        return self._model_stable