from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from ews_app.converter_interfaces.converter_model_article_to_model_event_interface import \
                                                           ConverterArticleToEventInterface


class ConverterBinanceArticleToBinanceEvent(ConverterArticleToEventInterface):
    
    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance = logger
        self._model_event     = ModelBinanceEvent

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def model_event(self):
        return self._model_event