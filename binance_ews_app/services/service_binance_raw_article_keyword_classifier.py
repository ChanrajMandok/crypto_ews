from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.store.stores_binance import \
                                        StoreBinance
from binance_ews_app.model.model_binance_article import \
                                       ModelBinanceArticle                       
from binance_ews_app.model.model_binance_article_raw import \
                                        ModelBinanceArticleRaw      
from binance_ews_app.converters.converter_binance_raw_article_to_binance_article \
                                 import ConverterBinanceRawArticleToBinanceArticle
from ews_app.service_interfaces.service_model_raw_article_keyword_classifier_interface \
                          import ServiceBinanceRawArticleKeywordClassifierInterface

@singleton
class ServiceBinanceRawArticleKeywordClassifier(ServiceBinanceRawArticleKeywordClassifierInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance     = logger
        self._model_article       = ModelBinanceArticle
        self._model_article_raw   = ModelBinanceArticleRaw
        self._store               = StoreBinance.store_db_binance_last_updated
        self._converter           = ConverterBinanceRawArticleToBinanceArticle()

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    def store(self):
        return self._store
    
    def converter_ra_to_a(self):
        return self._converter