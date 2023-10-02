import json

from django.test import TestCase
from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from binance_ews_app.model.model_binance_article_raw import \
                                       ModelBinanceArticleRaw
from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from binance_ews_app.model.model_binance_article import ModelBinanceArticle
from binance_ews_app.converters.converter_dict_to_binance_article_raw import \
                                              ConverterDictToBinanceArticleRaw
from binance_ews_app.converters.converter_binance_article_to_binance_event import \
                                              ConverterBinanceArticleToBinanceEvent
from binance_ews_app.converters.converter_binance_raw_article_to_binance_article import \
                                               ConverterBinanceRawArticleToBinanceArticle


class TestBinanceConvertersTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        self.__converter_dict_to_model_binance_article_raw      = ConverterDictToBinanceArticleRaw()
        self.__converter_binance_article_to_binance_event       = ConverterBinanceArticleToBinanceEvent()
        self.__converter_binance_raw_article_to_binance_article = ConverterBinanceRawArticleToBinanceArticle()

    def _build_model_binance_article_raw(self):
        filepath = r'./binance_ews_app/test/data/binance_article_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        return ModelBinanceArticleRaw(
                                      id           = data_dict['id'],
                                      url          = None,
                                      code         = data_dict['code'],
                                      title        = data_dict['title'],
                                      release_date = data_dict['releaseDate']
                                     )

    def test_converter_dict_to_model_binance_article_raw(self):
        filepath = r'./binance_ews_app/test/data/binance_article_dict.json'
        f = open (filepath, "r")
        article_dict = json.loads(f.read())

        model_article_raw = \
            self.__converter_dict_to_model_binance_article_raw.convert(article_dict)

        self.assertIsNotNone(model_article_raw)
        self.assertTrue(isinstance(model_article_raw, ModelBinanceArticleRaw))

    def test_converter_binance_raw_article_to_binance_article(self):

        alert_priority = EnumPriority.HIGH.name
        alert_category = EnumHighAlertWarningKeyWords.TOKEN_REMOVAL

        model_raw_article = \
            self._build_model_binance_article_raw()
        
        model_binance_article = \
            self.__converter_binance_raw_article_to_binance_article.convert(
                alert_priority = alert_priority,
                alert_category = alert_category,
                model_raw_article = model_raw_article
            )
        
        self.assertIsNotNone(model_binance_article)
        self.assertTrue(isinstance(model_binance_article, ModelBinanceArticle))

    def test_converter_binance_article_to_binance_event(self):

        filepath = r'./binance_ews_app/test/data/binance_html.json'
        f = open (filepath, "r")
        html_binance = json.loads(f.read())

        source = EnumSource.BINANCE

        model_raw_article = self._build_model_binance_article_raw()

        model_binance_article = \
                                ModelBinanceArticle(
                                    id             = 999999,
                                    html           = html_binance,
                                    raw_article    = model_raw_article,
                                    alert_priority = EnumPriority.HIGH.name,
                                    alert_category = EnumHighAlertWarningKeyWords.TOKEN_REMOVAL,
                                    url            = 'https://www.binance.com/en/support/announcement/testing_exmaple',
                                )

        model_binance_event = \
            self.__converter_binance_article_to_binance_event.convert(
                trading_affected = True,
                source           = source,   
                network_tokens   = ['ETH'],
                article          = model_binance_article, 
                important_dates  = [1693495466000, 1693495446000, 1693495406000],
                h_spot_tickers   = ['ALGO/BTC', 'ALICE/BTC', 'ALICE/USDT', 'AMP/USDT', 'ANKR/BTC', 'APE/BTC', 'API3/USDT']
            )
        
        self.assertIsNotNone(model_binance_event)
        self.assertTrue(isinstance(model_binance_event, ModelBinanceEvent))