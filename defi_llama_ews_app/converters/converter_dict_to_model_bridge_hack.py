from defi_llama_ews_app.converters import logger
from defi_llama_ews_app.model.model_defi_llama_bridge_hack import \
                                           ModelDefiLlamaBridgeHack
from ews_app.converter_interfaces.converter_dict_to_model_defi_bridge_hack_interface import \
                                                      ConverterDictToModelBridgeHackInterface


class ConverterDictToModelBridgeHack(ConverterDictToModelBridgeHackInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance = logger
        self._model_hack      = ModelDefiLlamaBridgeHack
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def logger_instance(self):
        return self._logger_instance

    @property
    def hack_amount_key(self) -> str:
        return 'amount'

    @property
    def release_date_key(self) -> str:
        return 'date'
        
    @property
    def url_key(self) -> str:
        return 'link'
        
    @property
    def protocol_key(self) -> str:
        return 'name'

    @property
    def exploit_key(self) -> str:
        return 'technique'
    
    @property
    def blockchain_key(self) -> str:
        return 'chains'
    
    def model_hack(self):
        return self._model_hack
    