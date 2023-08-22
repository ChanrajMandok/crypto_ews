import os
import requests

from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.decorator.decorator_binance_headers_required import binance_headers_required
from binance_ews_app.decorator.decorator_binance_urls_required import binance_article_url_required
from binance_ews_app.services.service_binance_article_handler import ServiceBinanceArticleHandler


@singleton
class ServiceBinanceyNewsHtmlRetriever:
    
    """
    Service iterates over the articles which have been found to have important keywords & are within 
    date range. It will output the important events with dates which can be used create alerts.  
    """
    

    def __init__(self) -> None:
        self.service_binance_article_handler = ServiceBinanceArticleHandler()

    @binance_headers_required
    @binance_article_url_required
    def retrieve(self,
                 articles: list[dict],
                 binance_headers=None,
                 binance_news_list_url=None,
                 binance_article_base_url=None):

        ssl_verify = False if os.environ.get('SSL_VERIFY', 'True') == "False" else True
        timeout = int(os.environ.get('TIMEOUT', 10))

        session = requests.Session()
        session.verify = ssl_verify
        
        articles_to_remove = []

        for article in articles:
            code = article.get('code', '')
            title = article.get('title', '').replace(' ', '-')
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
                logger.info(f"{self.__class__.__name__} - ERROR: {str(e)}")
                continue

            if response.status_code - (response.status_code % 100) != 200:
                logger.info(f"{self.__class__.__name__} {response.status_code} - ERROR: " +
                            f"Failed to get a response from Binance for URL: {url}. {response.content}")
                continue  # If the status code is not in the 200 range, we skip processing for this article.

            handled = self.service_binance_article_handler.handle(
                article_html_content=response.content, title=title)
            

            if handled['pop']:
                articles_to_remove.append(article)
            else:
                article.update(handled)
                article.extend({'url':url})
                
        for article in articles_to_remove:
            articles.remove(article)

        return articles
