import os
import time
import requests

from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_article_raw import ModelBinanceArticleRaw
from binance_ews_app.decorator.decorator_binance_headers_required import \
    binance_headers_required
from binance_ews_app.decorator.decorator_binance_urls_required import \
    binance_article_url_required
from binance_ews_app.converters.converter_dict_to_model_binance_article_raw import \
    ConverterDictToModelBinanceArticleRaw


@singleton
class ServiceBinanceRawArticleRetriever:
    """
    Services finds the latest articles headlines released from Binance announcements Page 
    """

    def __init__(self) -> None:
        self.__converter = ConverterDictToModelBinanceArticleRaw()

    @binance_headers_required
    @binance_article_url_required
    def retrieve(self, binance_headers, binance_news_dict_url,
                 binance_article_base_url=None) -> list[ModelBinanceArticleRaw]:

        tries = 0
        ssl_env = os.environ.get('SSL_VERIFY', 'True')
        ssl_verify = False if ssl_env == "False" else True
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
                code_group = response.status_code - (response.status_code % 100)
                if code_group != 200:
                    logger.error(
                        f"{self.__class__.__name__} {response.status_code} - "
                        f"ERROR: Failed to get a response from Binance. "
                        f"{response.content}")
                    time.sleep(5)
                    tries += 1
                    continue

                response_json = response.json()
                data = response_json.get('data')
                if not data:
                    msg = (f"{self.__class__.__name__} - ERROR: 'data' attribute "
                           f"missing in the {binance_news_dict_url} response.")
                    logger.error(msg)
                    tries += 1
                    continue

                catalogues = data.get('catalogs')
                if not catalogues:
                    msg = (f"{self.__class__.__name__} - ERROR: 'catalogs' "
                           f"attribute missing in {binance_news_dict_url} response.")
                    logger.error(msg)
                    tries += 1
                    continue

                binance_raw_articles = []
                for catalog in catalogues:
                    if not isinstance(catalog, dict):
                        msg = (f"{self.__class__.__name__} - ERROR: Unexpected "
                               f"catalog format in {binance_news_dict_url} response.")
                        logger.error(msg)
                        continue

                    articles = catalog.get('articles')
                    if not articles:
                        msg = (f"{self.__class__.__name__} - ERROR: 'articles' "
                               f"attribute missing in a catalog from {binance_news_dict_url} response.")
                        logger.error(msg)
                        continue
                    if not isinstance(articles, list):
                        msg = (f"{self.__class__.__name__} - ERROR: Unexpected "
                               f"'articles' format in a catalog from {binance_news_dict_url} response.")
                        logger.error(msg)
                        continue

                    # Convert to model_raw_bianance_article
                    articles_model = [self.__converter.convert(article) for article in articles]
                    binance_raw_articles.extend(articles_model)

                return binance_raw_articles

            except requests.RequestException as e:
                msg = (f"{self.__class__.__name__} - ERROR: {str(e)} - "
                       f"try {tries} failed")
                logger.error(msg)
                time.sleep(5)
                tries += 1

        return []  # Return an empty list if all tries fail