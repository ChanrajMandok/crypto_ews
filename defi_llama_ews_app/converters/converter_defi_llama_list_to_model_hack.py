from defi_llama_ews_app.converters import logger
from defi_llama_ews_app.model.model_defi_llama_hack import ModelDefiLlamaHack
from ews_app.converter_interfaces.converter_list_to_model_defi_hack_interface \
                                    import ConverterListToModelHackRawInterface


class ConverterDefiLlamaListToModelHack(ConverterListToModelHackRawInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance = logger
        self._model_hack      = ModelDefiLlamaHack
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def protocol_list_index(self) -> int:
        return 0

    @property
    def release_date_list_index(self) -> int:
        return 1

    @property
    def hacked_amount_list_index(self) -> int:
        return 2

    @property
    def blockchain_list_index(self) -> int:
        return 3

    @property
    def exploit_list_index(self) -> int:
        return 5

    @property
    def url_list_index(self) -> int:
        return 6
    
    def model_hack(self):
        return self._model_hack 
