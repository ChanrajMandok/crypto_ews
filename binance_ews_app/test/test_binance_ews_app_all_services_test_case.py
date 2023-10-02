from django.test import TestCase
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw
from binance_ews_app.services.service_binance_raw_article_retriever import \
                                           ServiceBinanceRawArticleRetriever
from binance_ews_app.services.service_binance_article_html_retriever import \
                                           ServiceBinanceArticleHtmlRetriever
from binance_ews_app.services.service_binance_raw_article_keyword_classifier import \
                                            ServiceBinanceRawArticleKeywordClassifier


class TestBinanceEwsAppAllServicesTestCase(TestCase):

    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()

    def test_service_raw_article_retriever(self):
        try:
            service_raw_article_retriever = ServiceBinanceRawArticleRetriever()
            articles = service_raw_article_retriever.retrieve()
            self.assertIsNotNone(articles)
            self.assertTrue(isinstance(articles, list))
            self.assertTrue(all(isinstance(item, ModelBinanceArticleRaw) for item in articles))
        except Exception as e:
            raise Exception(f"Failure in service_raw_article_retriever: {e}")

    def test_service_raw_article_keyword_classifier(self):
        try:
            service_raw_article_retriever = ServiceBinanceRawArticleRetriever()
            articles = service_raw_article_retriever.retrieve()

            service_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
            key_articles = service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            self.assertIsNotNone(key_articles)
        except Exception as e:
            raise Exception(f"Failure in service_raw_article_keyword_classifier: {e}")

    def test_service_article_html_retriever(self):
        try:
            service_raw_article_retriever = ServiceBinanceRawArticleRetriever()
            articles = service_raw_article_retriever.retrieve()

            service_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()
            key_articles = service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)

            service_article_html_retriever = ServiceBinanceArticleHtmlRetriever()
            model_event_objects = service_article_html_retriever.retrieve(key_articles, test=True)
            self.assertIsNotNone(model_event_objects)
        except Exception as e:
            raise Exception(f"Failure in service_article_html_retriever: {e}")