from django.test import TestCase
from okx_ews_app.services.service_okx_raw_article_retriever import \
                                        ServiceOkxRawArticleRetriever
from okx_ews_app.services.service_okx_raw_article_keyword_classifier \
                            import ServiceOkxRawArticleKeywordClassifier


class TestServiceOkxRawArticleRetrieverTestCase(TestCase):

    def setUp(self):
        self.service_okx_raw_article_retriever      = ServiceOkxRawArticleRetriever()
        self.service_raw_article_keyword_classifier = ServiceOkxRawArticleKeywordClassifier()

    def test(self):

        articles = self.service_okx_raw_article_retriever.retrieve()
        self.assertIsNotNone(articles)

        key_articles = self.service_raw_article_keyword_classifier().classify_articles(raw_articles=articles)
        self.assertIsNotNone(articles)