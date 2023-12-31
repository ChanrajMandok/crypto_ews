from django.test import TestCase

from ews_app.model.model_order_book import ModelOrderBook
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from okx_ews_app.services.service_okx_orderbook_retriever import \
                                      ServiceOkxOrderbookRetriever
from okx_ews_app.services.service_okx_raw_article_retriever import \
                                       ServiceOkxRawArticleRetriever
from okx_ews_app.model.model_okx_article_raw import ModelOkxArticleRaw
from okx_ews_app.services.service_okx_article_html_retriever import \
                                       ServiceOkxArticleHtmlRetriever
from okx_ews_app.services.service_okx_raw_article_keyword_classifier import \
                                        ServiceOkxRawArticleKeywordClassifier


class TestOkxEwsAppAllServicesTestCase(TestCase):

    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()

    def test_service_raw_article_retriever(self):
        try:
            service_raw_article_retriever = ServiceOkxRawArticleRetriever()
            articles = service_raw_article_retriever.retrieve()
            self.assertIsNotNone(articles)
            self.assertTrue(isinstance(articles, list))
            self.assertTrue(all(isinstance(item, ModelOkxArticleRaw) for item in articles))
        except Exception as e:
            raise Exception(f"Failure in service_raw_article_retriever: {e}")

    def test_service_raw_article_keyword_classifier(self):
        try:
            service_raw_article_retriever = ServiceOkxRawArticleRetriever()
            articles = service_raw_article_retriever.retrieve()

            service_raw_article_keyword_classifier = ServiceOkxRawArticleKeywordClassifier()
            key_articles = service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)
            self.assertIsNotNone(key_articles)
        except Exception as e:
            raise Exception(f"Failure in service_raw_article_keyword_classifier: {e}")

    def test_service_article_html_retriever(self):
        try:
            service_raw_article_retriever = ServiceOkxRawArticleRetriever()
            articles = service_raw_article_retriever.retrieve()

            service_raw_article_keyword_classifier = ServiceOkxRawArticleKeywordClassifier()
            key_articles = service_raw_article_keyword_classifier.classify_articles(raw_articles=articles)

            service_article_html_retriever = ServiceOkxArticleHtmlRetriever()
            model_event_objects = service_article_html_retriever.retrieve(key_articles, test=True)
            self.assertIsNotNone(model_event_objects)
        except Exception as e:
            raise Exception(f"Failure in service_article_html_retriever: {e}")
        
    def test_service_okx_orderbook_retriever(self):
        try:
            service_okx_orderbook_retriever = ServiceOkxOrderbookRetriever()
            spot_asset_orderbooks = service_okx_orderbook_retriever.retrieve()
            
            self.assertIsNotNone(spot_asset_orderbooks)
            self.assertTrue(isinstance(spot_asset_orderbooks, dict))
            self.assertTrue(list(spot_asset_orderbooks.values())[0], ModelOrderBook)
        except Exception as e:
            raise Exception(f"Failure in service_okx_orderbook_retriever: {e}")