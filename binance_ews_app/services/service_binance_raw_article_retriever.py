from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_article_raw import \
                                        ModelBinanceArticleRaw
from binance_ews_app.converters.converter_dict_to_binance_article_raw \
                                import ConverterDictToBinanceArticleRaw
from binance_ews_app.decorator.decorator_binance_urls_required import \
                                             binance_article_url_required
from binance_ews_app.decorator.decorator_binance_headers_required import \
                                                   binance_headers_required
from ews_app.service_interfaces.service_model_raw_article_interface import \
                                          ServiceRawArticleRetrieverInterface


@singleton
class ServiceBinanceRawArticleRetriever(ServiceRawArticleRetrieverInterface):

    @binance_headers_required
    @binance_article_url_required
    def __init__(self,
                 binance_headers,
                 binance_news_dict_url,
                 binance_article_base_url,
                 **kwargs) -> None:
        super().__init__() 
        self._logger_instance     = logger
        self._headers             = binance_headers
        self._dict_url            = binance_news_dict_url
        self._model_article_raw   = ModelBinanceArticleRaw
        self._base_url            = binance_article_base_url
        self._converter           = ConverterDictToBinanceArticleRaw()

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
        return 'catalogs'
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    def retrieve(self) -> list[ModelBinanceArticleRaw]:
        try:
            catalogues = super().retrieve()
            binance_raw_articles = []
            for catalog in catalogues:
                if not isinstance(catalog, dict):
                    msg = (f"{self.__class__.__name__} - ERROR: Unexpected "
                            f"catalog format in {self.dict_url} response.")
                    logger.error(msg)
                    continue

                articles = catalog.get('articles')
                if not articles:
                    msg = (f"{self.__class__.__name__} - ERROR: 'articles' "
                            f"attribute missing in a catalog from {self.dict_url} response.")
                    logger.error(msg)
                    continue
                if not isinstance(articles, list):
                    msg = (f"{self.__class__.__name__} - ERROR: Unexpected "
                            f"'articles' format in a catalog from {self.dict_url} response.")
                    logger.error(msg)
                    continue

                # Convert to model_raw_bianance_article
                articles_model = [self._converter.convert(article) for article in articles]
                binance_raw_articles.extend(articles_model)

            return binance_raw_articles

        except Exception as e:
            msg = (f"{self.class_name} - ERROR: {str(e)} - ")
            logger.error(msg)

        return []