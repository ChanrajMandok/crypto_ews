import os
import requests

from time import sleep
from random import randint
from datetime import datetime
from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_article import ModelBinanceArticle
from binance_ews_app.decorator.decorator_binance_urls_required import \
                                               binance_article_url_required
from binance_ews_app.services.service_binance_article_html_handler import \
                                             ServiceBinanceArticleHtmlHandler
from binance_ews_app.decorator.decorator_binance_headers_required import \
                                                    binance_headers_required


@singleton
class ServiceBinanceArticleHtmlRetriever:
    
    """
    Service iterates over the articles which have been found to have important 
    keywords & are within date range and retrieves the html of the article. 
    """

    def __init__(self) -> None:
        self.__service_binance_article_html_handler = ServiceBinanceArticleHtmlHandler()

    @binance_headers_required
    @binance_article_url_required
    def retrieve(self,
                 articles: list[ModelBinanceArticle],
                 binance_headers=None,
                 binance_news_dict_url=None,
                 binance_article_base_url=None):

        today = int(datetime.now().timestamp())*1000
        timeout = int(os.environ.get('TIMEOUT', 10))
        ssl_verify = False if os.environ.get('SSL_VERIFY', 'True') == "False" else True
        
        
        session = requests.Session()
        session.verify = ssl_verify
        
        model_event_list = []
        
        for article_object in articles:
            sleep(randint(1,3))  # Random sleep between 1 and 3 seconds

            raw_article = article_object.raw_article
            code = raw_article.code
            id = raw_article.id
            title = raw_article.title.replace(' ', '-')
            url = f"{binance_article_base_url}{code}"

            try:
                response = session.get(
                    url=url,
                    headers=binance_headers,
                    timeout=timeout
                )

                if response.status_code == 429:
                    logger.info(f"{self.__class__.__name__} {response.status_code} - INFO: " +
                                f"Switching to backup URL due to rate limit for: {url}.")
                    url = f"{binance_article_base_url}-{title}-{code}"
                    response = session.get(
                        url=url,
                        headers=binance_headers,
                        timeout=timeout
                    )

            except requests.RequestException as e:
                logger.error(f"{self.__class__.__name__} - ERROR: {str(e)}")
                continue

            if response.status_code - (response.status_code % 100) != 200:
                logger.error(f"{self.__class__.__name__} {response.status_code} - ERROR: " +
                            f"Failed to get a response from Binance for URL: {url}. {response.content}")
                continue
            
            decoded_content = response.content.decode('utf-8')

            if not decoded_content.lstrip().startswith(('<!DOCTYPE', '<html')) or \
                '<body' not in decoded_content:
                logger.error(f"{self.__class__.__name__} - ERROR: Invalid HTML received for URL: {url}.")
                continue
            
            article_object.url = url
            article_object.html = response.content
            
            model_event = self.__service_binance_article_html_handler.handle(article_object)
            if max(model_event.important_dates) > today:
                model_event_list.append(model_event)           
            
        return model_event_list

        