from okx_ews_app.services import logger
from okx_ews_app.store.stores_okx import \
                                   StoreOkx
from okx_ews_app.model.model_okx_article import \
                                   ModelOkxArticle                       
from okx_ews_app.model.model_okx_article_raw import \
                                    ModelOkxArticleRaw      
from okx_ews_app.converters.converter_okx_raw_article_to_okx_article \
                              import ConverterOkxRawArticleToOkxArticle
from ews_app.service_interfaces.service_raw_article_keyword_classifier_interface \
                         import ServiceBinanceRawArticleKeywordClassifierInterface

class ServiceOkxRawArticleKeywordClassifier(ServiceBinanceRawArticleKeywordClassifierInterface):

    def __init__(self) -> None:
        super().__init__() 
        self._logger_instance     = logger
        self._model_article       = ModelOkxArticle
        self._model_article_raw   = ModelOkxArticleRaw
        self._store               = StoreOkx.store_db_okx_last_updated
        self._converter           = ConverterOkxRawArticleToOkxArticle()

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    def store(self):
        return self._store
    
    def model_article_raw(self):
        return self._model_article_raw   

    def model_article(self):
        return self._model_article       
    
    def converter_ra_to_a(self):
        return self._converter