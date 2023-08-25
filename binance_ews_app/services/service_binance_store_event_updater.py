from binance_ews_app.services import logger

from binance_ews_app.store.stores_binance import StoresBinance
from binance_ews_app.services.service_binance_raw_article_retriever import ServiceBinanceRawArticleRetriever
from binance_ews_app.services.service_binance_article_html_retriever import ServiceBinanceArticleHtmlRetriever
from binance_ews_app.services.service_binance_raw_article_keyword_classifier import ServiceBinanceRawArticleKeywordClassifier


class ServiceStoreEventUpdater:
    
    def __init__(self) -> None:
        self.__service_binance_raw_article_retriever = ServiceBinanceRawArticleRetriever()
        self.__service_binance_article_html_retriever = ServiceBinanceArticleHtmlRetriever()
        self.__service_binance_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
        
    def main(self):
        try:
            # retrieve all recent news articles & announcements from binance
            articles = self.__service_binance_raw_article_retriever.retrieve()
            # filter news articles & announcements for specific values
            key_articles = self.__service_binance_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            # now pull html of articles from binance
            articles_with_html = self.__service_binance_article_html_retriever.retrieve(key_articles)
            # create store and when relevent updates occur create webhook which notifies relevent parties. 
            [StoresBinance.store_binance_events.add(key=x.id, instance=x) for x in articles_with_html]
            
        except Exception as e:
            logger.error(e)