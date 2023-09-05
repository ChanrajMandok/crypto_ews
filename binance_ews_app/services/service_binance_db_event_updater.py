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
from binance_ews_app.services.service_send_binance_event_to_ms_teams import \
                                         ServiceSendModelBinanceEventToMsTeams
from binance_ews_app.services.service_binance_raw_article_keyword_classifier \
                              import ServiceBinanceRawArticleKeywordClassifier


class ServiceDbEventUpdater:
    
    def __init__(self) -> None:
        self.__service_raw_article_retriever          = ServiceBinanceRawArticleRetriever()
        self.__service_article_html_retriever         = ServiceBinanceArticleHtmlRetriever()
        self.__service_send_binance_event_to_ms_teams = ServiceSendModelBinanceEventToMsTeams()
        self.__store_db_binance_last_updated          = StoreBinance.store_db_binance_last_updated
        self.__service_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
        
    def update_db(self):
        try:
            # Retrieve all recent news articles & announcements from binance
            articles = self.__service_raw_article_retriever.retrieve()
            
            # Filter news articles & announcements for specific values
            key_articles = self.__service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            
            # Now pull HTML of articles from binance
            model_event_objects = self.__service_article_html_retriever.retrieve(key_articles)

            now = int(datetime.now().timestamp()) * 1000
            # If there are no model event objects, exit early.
            if not model_event_objects:
                ts = ModelDbBinanceLastUpdated(last_updated=now)
                self.__store_db_binance_last_updated.set(ts)
                return

            # Check for duplicates and filter them out using the 'id' field
            existing_ids = ModelBinanceEvent.objects.filter(id__in=[x.id for x in model_event_objects]).values_list('id', flat=True)
            
            new_events = [event for event in model_event_objects if event.id not in existing_ids]
            
            # Save to DB and send messages for new events
            for event in new_events:
                event.save()
                self.__service_send_binance_event_to_ms_teams.send_message(event.ms_teams_message)

            ts = ModelDbBinanceLastUpdated(last_updated=now)
            self.__store_db_binance_last_updated.set(ts)

        except Exception as e:
            logger.error(e)

            
            
            
            