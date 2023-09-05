from okx_ews_app.converters import logger

from okx_ews_app.model.model_okx_article import \
                                       ModelOkxArticle
from okx_ews_app.model.model_okx_article_raw import \
                                    ModelOkxArticleRaw
from ews_app.converter_interfaces.converter_model_raw_article_to_model_article_interface \
                                    import ConverterModelRawArticleToModelArticleInterface


class ConverterOkxRawArticleToOkxArticle(ConverterModelRawArticleToModelArticleInterface):
    """
    Converts a raw Okx article by adding alert_priority and alert_category
    to create/update an instance of ModelOkxArticle.
    """
    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance    = logger
        self._model_article      = ModelOkxArticle
        self._model_article_raw  = ModelOkxArticleRaw

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def model_article_raw(self):
        return self._model_article_raw   

    def model_article(self):
        return self._model_article