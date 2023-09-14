from ews_app.converters import logger
from ews_app.converter_interfaces.converter_model_hack_to_model_event_interface \
                                    import ConverterModelHackToModelEventInterface
from defi_llama_ews_app.model.model_defi_bridge_hack_event import ModelDefiBridgeHackEvent
from defi_llama_ews_app.model.model_defi_llama_bridge_hack import ModelDefiLlamaBridgeHack


class ConverterModelDefiBridgeHackToModelEvent(ConverterModelHackToModelEventInterface):
    
    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._model_hack      = ModelDefiLlamaBridgeHack
        self._model_event     = ModelDefiBridgeHackEvent

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def logger_instance(self):
        return self._logger_instance
    
    def model_event(self):
        return self._model_event
    
    def model_hack(self):
        return self._model_hack 