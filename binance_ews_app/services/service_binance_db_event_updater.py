from datetime import datetime

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_event import \
                                        ModelBinanceEvent
from binance_ews_app.store.stores_binance import StoreBinance
from binance_ews_app.model.model_db_binance_last_updated import \
                                        ModelDbBinanceLastUpdated
from binance_ews_app.services.service_binance_raw_article_retriever import \
                                            ServiceBinanceRawArticleRetriever
from binance_ews_app.services.service_binance_article_html_retriever import \
                                            ServiceBinanceArticleHtmlRetriever
from binance_ews_app.services.service_binance_raw_article_keyword_classifier import \
                                            ServiceBinanceRawArticleKeywordClassifier


class ServiceDbEventUpdater:
    
    def __init__(self) -> None:
        self.__service_raw_article_retriever          = ServiceBinanceRawArticleRetriever()
        self.__service_article_html_retriever         = ServiceBinanceArticleHtmlRetriever()
        self.__store_db_binance_last_updated          = StoreBinance.store_db_binance_last_updated
        self.__service_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
        
    def update_db(self):
        try:
            today = int(datetime.now().timestamp())*1000
            ts = ModelDbBinanceLastUpdated(last_updated=today)
            # retrieve all recent news articles & announcements from binance
            articles = self.__service_raw_article_retriever.retrieve()
            # filter news articles & announcements for specific values
            key_articles = self.__service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            # now pull html of articles from binance
            model_event_objects = self.__service_article_html_retriever.retrieve(key_articles)
            # save to db
            ModelBinanceEvent.objects.bulk_create(model_event_objects, ignore_conflicts=True)
            self.__store_db_binance_last_updated.set(ts)

        except Exception as e:
            logger.error(e)
            
            
            
            
            