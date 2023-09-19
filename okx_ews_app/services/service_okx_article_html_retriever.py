from singleton_decorator import singleton

from okx_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from okx_ews_app.model.model_okx_event import ModelOkxEvent
from okx_ews_app.decorator.decorator_okx_urls_required import \
                                       okx_article_url_required
from okx_ews_app.model.model_okx_article import ModelOkxArticle
from okx_ews_app.decorator.decorator_okx_headers_required import \
                                              okx_headers_required
from okx_ews_app.services.service_okx_article_html_handler import \
                                        ServiceOkxArticleHtmlHandler
from ews_app.service_interfaces.service_model_article_html_retriever_interface \
                                import ServiceModelArticleHtmlRetrieverInterface


@singleton
class ServiceOkxArticleHtmlRetriever(ServiceModelArticleHtmlRetrieverInterface):
    
    """
    Service iterates over the articles which have been found to have important 
    keywords & are within date range and retrieves the html of the article. 
    """
    @okx_headers_required
    @okx_article_url_required
    def __init__(self,
                 okx_headers,
                 okx_article_base_url,
                 **kwargs) -> None:
        super().__init__() 
        self._logger_instance     = logger
        self._headers             = okx_headers
        self._model_event         = ModelOkxEvent
        self._model_article       = ModelOkxArticle
        self._base_url            = okx_article_base_url
        self._article_handler     = ServiceOkxArticleHtmlHandler()

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
        return EnumSource.OKX