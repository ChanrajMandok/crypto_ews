from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_article import \
                                       ModelBinanceArticle
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw
from ews_app.converter_interfaces.converter_model_raw_article_to_model_article_interface \
                                    import ConverterModelRawArticleToModelArticleInterface


class ConverterBinanceRawArticleToBinanceArticle(ConverterModelRawArticleToModelArticleInterface):
    """
    Converts a raw Binance article by adding alert_priority and alert_category
    to create/update an instance of ModelBinanceArticle.
    """

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance    = logger
        self._model_article      = ModelBinanceArticle
        self._model_article_raw  = ModelBinanceArticleRaw

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