from coinmarketcap_ews_app.converters import logger
from coinmarketcap_ews_app.model.model_token_liquidity_event import \
                                             ModelTokenLiquidityEvent
from ews_app.converter_interfaces.converter_dict_to_model_event_interface import \
                                                ConverterDictToModelEventInterface


class ConverterDictToModelTokenLiquidityEvent(ConverterDictToModelEventInterface):
    
    def __init__(self) -> None:
            super().__init__() 
            self._logger_instance = logger
            self._model_event      = ModelTokenLiquidityEvent
        
    @property
    def class_name(self) -> str:
            return f"{self.__class__.__name__}"

    @property
    def logger_instance(self):
            return self._logger_instance

    def model_event(self):
        return self._model_event