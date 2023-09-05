from okx_ews_app.converters import logger
from okx_ews_app.model.model_okx_event import \
                                       ModelOkxEvent
from ews_app.converter_interfaces.converter_model_article_to_model_event_interface \
                                              import ConverterArticleToEventInterface


class ConverterOkxArticleToOkxEvent(ConverterArticleToEventInterface):
    
    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance = logger
        self._model_event = ModelOkxEvent

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def model_event(self):
        return self._model_event