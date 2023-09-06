import requests

from okx_ews_app.services import logger
from okx_ews_app.model.model_okx_article_raw import ModelOkxArticleRaw 
from okx_ews_app.decorator.decorator_okx_urls_required import \
                                       okx_article_url_required
from okx_ews_app.decorator.decorator_okx_headers_required import \
                                              okx_headers_required
from okx_ews_app.converters.converter_dict_to_okx_article_raw import \
                                      ConverterDictToModelokxArticleRaw
from ews_app.service_interfaces.service_model_raw_article_interface import \
                                          ServiceRawArticleRetrieverInterface

class ServiceOkxRawArticleRetriever(ServiceRawArticleRetrieverInterface):

    @okx_headers_required
    @okx_article_url_required
    def __init__(self, 
                 okx_headers,
                 okx_news_dict_url,
                 okx_article_base_url=None, 
                 **kwargs) -> None:
        super().__init__() 
        self._logger_instance     = logger
        self._headers             = okx_headers
        self._dict_url            = okx_news_dict_url
        self._model_article_raw   = ModelOkxArticleRaw
        self._base_url            = okx_article_base_url
        self.__converter          = ConverterDictToModelokxArticleRaw()
        
    @property
    def url_headers(self):
        return self._headers
    
    @property
    def base_url(self):
        return self._base_url
    
    @property
    def dict_url(self):
        return self._dict_url
    
    @property
    def nested_key_1(self) -> str:
        return 'notices'
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    def retrieve(self) -> list[ModelOkxArticleRaw]:

        try:
            notices = super().retrieve()
            okx_raw_articles = []
            for noitce in notices:
                if not isinstance(noitce, dict):
                    msg = (f"{self.__class__.__name__} - ERROR: Unexpected "
                            f"catalog format in {self.dict_url} response.")
                    logger.error(msg)
                    continue

                # Convert to model_raw_bianance_article
                articles_model = self.__converter.convert(noitce) 
                okx_raw_articles.append(articles_model)

            return okx_raw_articles

        except requests.RequestException as e:
            msg = (f"{self.class_name} - ERROR: {str(e)} - ")
            logger.error(msg)

        return []