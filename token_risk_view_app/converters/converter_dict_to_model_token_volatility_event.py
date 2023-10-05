from token_risk_view_app.converters import logger
from token_risk_view_app.model.model_token_volatility_event import ModelTokenVolatilityEvent
from ews_app.converter_interfaces.converter_dict_to_model_token_volatility_event_interface import \
                                                  ConverterDictToModelTokenVolatilityEventInterface


class ConverterDictToModelTokenVolatilityEvent(ConverterDictToModelTokenVolatilityEventInterface):
    
    def __init__(self) -> None:
            super().__init__() 
            self._logger_instance = logger
            self._model_event      = ModelTokenVolatilityEvent
        
    @property
    def class_name(self) -> str:
            return f"{self.__class__.__name__}"

    @property
    def logger_instance(self):
            return self._logger_instance

    def model_event(self):
        return self._model_event