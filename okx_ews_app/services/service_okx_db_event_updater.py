from okx_ews_app.services import logger
from okx_ews_app.store.stores_okx import StoreOkx

from okx_ews_app.services.service_okx_raw_article_retriever import \
                                        ServiceOkxRawArticleRetriever
from okx_ews_app.services.service_okx_article_html_retriever import \
                                        ServiceOkxArticleHtmlRetriever
from okx_ews_app.services.service_okx_raw_article_keyword_classifier \
                           import ServiceOkxRawArticleKeywordClassifier


class ServiceOkxDbEventUpdater:
    
    def __init__(self) -> None:
        self.__service_raw_article_retriever          = ServiceOkxRawArticleRetriever()
        self.__service_okx_article_html_retriever     = ServiceOkxArticleHtmlRetriever()
        self.__store_db_okx_last_updated              = StoreOkx.store_db_okx_last_updated
        self.__service_raw_article_keyword_classifier = ServiceOkxRawArticleKeywordClassifier()
        
    def update_db(self):
        try:
            # Retrieve all recent news articles & announcements from okx
            articles = self.__service_raw_article_retriever.retrieve()
            
            # Filter news articles & announcements for specific values
            key_articles = self.__service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            
            model_event_objects = self.__service_okx_article_html_retriever.retrieve(key_articles)

            print(model_event_objects)

        except Exception as e:
            logger.error(e)