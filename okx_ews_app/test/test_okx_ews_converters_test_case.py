import json

from django.test import TestCase

from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_priority import EnumPriority
from okx_ews_app.model.model_okx_event import ModelOkxEvent
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from okx_ews_app.model.model_okx_article import ModelOkxArticle    
from okx_ews_app.model.model_okx_article_raw import ModelOkxArticleRaw
from okx_ews_app.converters.converter_dict_to_okx_article_raw import \
                                          ConverterDictToOkxArticleRaw
from okx_ews_app.converters.converter_okx_article_to_okx_event import \
                                           ConverterOkxArticleToOkxEvent
from okx_ews_app.converters.converter_okx_raw_article_to_okx_article import \
                                            ConverterOkxRawArticleToOkxArticle


class TestOkxConvertersTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        self.__converter_dict_to_model_okx_article_raw      = ConverterDictToOkxArticleRaw()
        self.__converter_okx_article_to_okx_event           = ConverterOkxArticleToOkxEvent()
        self.__converter_okx_raw_article_to_okx_article     = ConverterOkxRawArticleToOkxArticle()

    def _build_model_okx_article_raw(self):
        filepath = r'./okx_ews_app/test/data/okx_article_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        return ModelOkxArticleRaw(
                                      id           = data_dict['sort'],
                                      url          = None,
                                      code         = data_dict['sort'],
                                      title        = data_dict['shareTitle'],
                                      release_date = data_dict['publishDate']
                                     )

    def test_converter_dict_to_model_okx_article_raw(self):
        filepath = r'./okx_ews_app/test/data/okx_article_dict.json'
        f = open (filepath, "r")
        article_dict = json.loads(f.read())

        model_article_raw = \
            self.__converter_dict_to_model_okx_article_raw.convert(article_dict)

        self.assertIsNotNone(model_article_raw)
        self.assertTrue(isinstance(model_article_raw, ModelOkxArticleRaw))

    def test_converter_okx_raw_article_to_okx_article(self):

        alert_priority = EnumPriority.HIGH.name
        alert_category = EnumHighAlertWarningKeyWords.TOKEN_REMOVAL

        model_raw_article = \
            self._build_model_okx_article_raw()
        
        model_okx_article = \
            self.__converter_okx_raw_article_to_okx_article.convert(
                alert_priority = alert_priority,
                alert_category = alert_category,
                model_raw_article = model_raw_article
            )
        
        self.assertIsNotNone(model_okx_article)
        self.assertTrue(isinstance(model_okx_article, ModelOkxArticle))

    def test_converter_okx_article_to_okx_event(self):

        filepath = r'./okx_ews_app/test/data/okx_html.json'
        f = open (filepath, "r")
        html_okx = json.loads(f.read())

        source = EnumSource.BINANCE

        model_raw_article = self._build_model_okx_article_raw()

        model_okx_article = \
                                ModelOkxArticle(
                                    id             = 999999,
                                    html           = html_okx,
                                    raw_article    = model_raw_article,
                                    alert_priority = EnumPriority.HIGH.name,
                                    alert_category = EnumHighAlertWarningKeyWords.TOKEN_REMOVAL,
                                    url            = 'https://www.okx.com/en/support/announcement/testing_exmaple',
                                )

        model_okx_event = \
            self.__converter_okx_article_to_okx_event.convert(
                trading_affected = True,
                source           = source,   
                network_tokens   = ['ETH'],
                article          = model_okx_article, 
                h_spot_tickers   = ['ALGO/BTC', 'ALICE/BTC', 'ALICE/USDT', 'AMP/USDT', 'ANKR/BTC', 'APE/BTC', 'API3/USDT'],
                important_dates  = [1693495466000, 1693495446000, 1693495406000]
            )
        
        self.assertIsNotNone(model_okx_event)
        self.assertTrue(isinstance(model_okx_event, ModelOkxEvent))