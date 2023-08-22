import os
import time 
import requests

from singleton_decorator import singleton
from binance_ews_app.services import logger
from binance_ews_app.decorator.decorator_binance_headers_required import binance_headers_required
from binance_ews_app.decorator.decorator_binance_urls_required import binance_article_url_required

@singleton
class ServiceBinanceNewsDictRetriever:
    
    """
    Services finds latest articles realeased from Binance anncouncments Page 
    """
    
    @binance_headers_required
    @binance_article_url_required
    def retrieve(self, 
                 binance_headers,
                 binance_news_list_url,
                 binance_article_base_url=None) -> list[dict]:
        
        tries = 0
        binance_news = {}

        ssl_verify = False if os.environ.get('SSL_VERIFY', 'True') == "False" else True
        timeout = int(os.environ.get('TIMEOUT', 10))
        
        while tries < 3:
            try:
                session = requests.Session()
                session.verify = ssl_verify
                
                response = session.get(
                    url=binance_news_list_url,
                    headers=binance_headers,
                    timeout=timeout
                )

                if response.status_code - (response.status_code % 100) != 200:
                    logger.info(f"{self.__class__.__name__} {response.status_code} - ERROR: " +
                                        f"Failed to get a response from Binance . {response.content}")
                    time.sleep(5)
                    tries += 1
                    continue
                
            except requests.RequestException as e:
                logger.info(f"{self.__class__.__name__} - ERROR: {str(e)} - try {tries} failed")
                time.sleep(5)
                tries += 1
                continue
                
            catalogues = response.json().get('data', {}).get('catalogs', [])
            
            return catalogues

        return binance_news