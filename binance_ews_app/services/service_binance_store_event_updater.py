from binance_ews_app.services import logger

from binance_ews_app.store.stores_binance import StoresBinance
from binance_ews_app.observers.observer_binance_store_event_updater import ObserverBinanceStoreEvent
from binance_ews_app.services.service_binance_raw_article_retriever import ServiceBinanceRawArticleRetriever
from binance_ews_app.services.service_binance_article_html_retriever import ServiceBinanceArticleHtmlRetriever
from binance_ews_app.services.service_send_binance_event_to_ms_teams import ServiceSendModelBinanceEventToMsTeams
from binance_ews_app.services.service_binance_raw_article_keyword_classifier import ServiceBinanceRawArticleKeywordClassifier


class ServiceStoreEventUpdater:
    
    def __init__(self) -> None:
        self.__service_binance_raw_article_retriever = ServiceBinanceRawArticleRetriever()
        self.__service_binance_article_html_retriever = ServiceBinanceArticleHtmlRetriever()
        self.__service_send_binance_event_to_ms_teams = ServiceSendModelBinanceEventToMsTeams()
        self.__service_binance_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
        
    def update_store(self):
        try:
            # retrieve all recent news articles & announcements from binance
            articles = self.__service_binance_raw_article_retriever.retrieve()
            # filter news articles & announcements for specific values
            key_articles = self.__service_binance_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            # now pull html of articles from binance
            model_event_objects = self.__service_binance_article_html_retriever.retrieve(key_articles)
            # create store and when relevent updates occur create webhook which notifies relevent parties. 
            [StoresBinance.store_binance_events.add(key=x.id, instance=x) for x in model_event_objects]
            [self.__service_send_binance_event_to_ms_teams.send_message(x.ms_teams_message) for x in model_event_objects]
            
        except Exception as e:
            logger.error(e)