from decimal import Decimal

from django.test import TestCase
from ews_app.model.model_order_book import ModelOrderBook
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw
from binance_ews_app.services.service_binance_orderbook_retriever import \
                                          ServiceBinanceOrderbookRetriever
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
        
    def test_service_binance_orderbook_retriever(self):
        
        try:
            # Initialize and retrieve
            service_binance_orderbook_retriever = ServiceBinanceOrderbookRetriever()
            wirex_asset_orderbooks = service_binance_orderbook_retriever.retrieve()

            # Check if wirex_asset_orderbooks is not None and is a dictionary
            self.assertIsNotNone(wirex_asset_orderbooks)
            self.assertTrue(isinstance(wirex_asset_orderbooks, dict))

            # Check if wirex_asset_orderbooks is not empty
            self.assertTrue(len(wirex_asset_orderbooks) > 0)

            # Iterate over items and check values
            for key, orderbook in wirex_asset_orderbooks.items():
                # Check if orderbook is of type ModelOrderBook
                self.assertIsInstance(orderbook, ModelOrderBook)

                # Check if bid price, bid volume, ask price, and ask volume are not zero
                self.assertNotEqual(orderbook.bid.price, Decimal('0'), f'bid.price for key {key} is zero.')
                self.assertNotEqual(orderbook.bid.volume, Decimal('0'), f'bid.volume for key {key} is zero.')
                self.assertNotEqual(orderbook.ask.price, Decimal('0'), f'ask.price for key {key} is zero.')
                self.assertNotEqual(orderbook.ask.volume, Decimal('0'), f'ask.volume for key {key} is zero.')

        except Exception as e:
            raise Exception(f"Failure in service_binance_orderbook_retriever: {e}")