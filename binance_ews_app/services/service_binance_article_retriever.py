import os
import time
import requests

from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_article_raw import ModelBinanceArticleRaw
from binance_ews_app.converters.converter_dict_to_model_binance_article import ConverterDictToModelBinanceArticle
from binance_ews_app.decorator.decorator_binance_headers_required import binance_headers_required
from binance_ews_app.decorator.decorator_binance_urls_required import binance_article_url_required


@singleton
class ServiceBinanceArticleRetriever:
    """
    Services finds the latest articles headlines released from Binance announcements Page 
    """

    def __init__(self) -> None:
        self.converter_dict_to_model_binance_article = ConverterDictToModelBinanceArticle()
    
    @binance_headers_required
    @binance_article_url_required
    def retrieve(self, 
                 binance_headers,
                 binance_news_dict_url,
                 binance_article_base_url=None) -> list[dict]:
        
        tries = 0
        ssl_verify = False if os.environ.get('SSL_VERIFY', 'True') == "False" else True
        timeout = int(os.environ.get('TIMEOUT', 10))
        
        while tries < 3:
            try:
                session = requests.Session()
                session.verify = ssl_verify
                
                response = session.get(
                    url=binance_news_dict_url,
                    headers=binance_headers,
                    timeout=timeout
                )

                if response.status_code - (response.status_code % 100) != 200: 
                    logger.error(f"{self.__class__.__name__} {response.status_code} - ERROR: " +
                                        f"Failed to get a response from Binance. {response.content}")
                    time.sleep(5)
                    tries += 1
                    continue
                
                response_json = response.json()

                data = response_json.get('data')
                if not data:
                    logger.error(f"{self.__class__.__name__} - ERROR: 'data' attribute missing in the {binance_news_dict_url} response.")
                    tries += 1
                    continue
                
                catalogues = data.get('catalogs')
                if not catalogues:
                    logger.error(f"{self.__class__.__name__} - ERROR: 'catalogs' attribute missing in 'data' {binance_news_dict_url} response.")
                    tries += 1
                    continue

                binance_articles = []
                for catalog in catalogues:
                    if not isinstance(catalog, dict):
                        logger.error(f"{self.__class__.__name__} - ERROR: Unexpected catalog format in {binance_news_dict_url} response.")
                        continue
                    
                    articles = catalog.get('articles')
                    if not articles:
                        logger.error(f"{self.__class__.__name__} - ERROR: 'articles' attribute missing in a catalog from {binance_news_dict_url} response.")
                        continue
                    if not isinstance(articles, list):
                        logger.error(f"{self.__class__.__name__} - ERROR: Unexpected 'articles' format in a catalog from {binance_news_dict_url} response.")
                        continue

                    list_model_articles = [self.converter_dict_to_model_binance_article.convert(article) for article in articles]
                    binance_articles.extend(list_model_articles)

                return binance_articles
                
            except requests.RequestException as e:
                logger.error(f"{self.__class__.__name__} - ERROR: {str(e)} - try {tries} failed")
                time.sleep(5)
                tries += 1

        return []  # Return an empty list if all tries fail
