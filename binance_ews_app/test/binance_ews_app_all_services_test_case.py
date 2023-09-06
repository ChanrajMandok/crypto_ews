from django.test import TestCase

from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv
from binance_ews_app.services.service_binance_raw_article_retriever import \
                                            ServiceBinanceRawArticleRetriever
from binance_ews_app.services.service_binance_article_html_retriever import \
                                            ServiceBinanceArticleHtmlRetriever
from ews_app.services.service_send_binance_event_to_ms_teams import \
                                        ServiceSendModelBinanceEventToMsTeams
from binance_ews_app.services.service_binance_raw_article_keyword_classifier import \
                                            ServiceBinanceRawArticleKeywordClassifier


class BinanceEwsAppAllServicesTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        self.__service_raw_article_retriever          = ServiceBinanceRawArticleRetriever()
        self.__service_article_html_retriever         = ServiceBinanceArticleHtmlRetriever()
        self.__service_send_binance_event_to_ms_teams = ServiceSendModelBinanceEventToMsTeams()
        self.__service_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
        
    def test(self):
        # retrieve all recent news articles & announcements from binance
        articles = self.__service_raw_article_retriever.retrieve()
        # filter news articles & announcements for specific values
        key_articles = self.__service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
        # now pull html of articles from binance
        model_event_objects = self.__service_article_html_retriever.retrieve(key_articles, test=True)
        [self.__service_send_binance_event_to_ms_teams.send_message(x.ms_teams_message) for x in model_event_objects]
            
    
        