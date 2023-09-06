from singleton_decorator import singleton

from binance_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from binance_ews_app.decorator.decorator_binance_urls_required import \
                                            binance_article_url_required
from binance_ews_app.decorator.decorator_binance_headers_required import \
                                                  binance_headers_required
from binance_ews_app.model.model_binance_article import ModelBinanceArticle
from binance_ews_app.services.service_binance_article_html_handler import \
                                             ServiceBinanceArticleHtmlHandler
from ews_app.service_interfaces.service_model_article_html_retriever_interface \
                                import ServiceModelArticleHtmlRetrieverInterface


@singleton
class ServiceBinanceArticleHtmlRetriever(ServiceModelArticleHtmlRetrieverInterface):
    
    """
    Service iterates over the articles which have been found to have important 
    keywords & are within date range and retrieves the html of the article. 
    """
    @binance_headers_required
    @binance_article_url_required
    def __init__(self,
                 binance_headers,
                 binance_article_base_url,
                 binance_news_dict_url=None) -> None:
        super().__init__() 
        self._logger_instance     = logger
        self._headers             = binance_headers
        self._model_event         = ModelBinanceEvent
        self._model_article       = ModelBinanceArticle
        self._base_url            = binance_article_base_url
        self._article_handler     = ServiceBinanceArticleHtmlHandler()

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def url_headers(self):
        return self._headers
    
    @property
    def base_url(self):
        return self._base_url
    
    def article_handler(self):
        return self._article_handler
    
    def source(self):
        return EnumSource.BINANCE