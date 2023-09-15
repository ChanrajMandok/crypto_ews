import json

from django.test import TestCase

from ews_app.enum.enum_priority import EnumPriority
from ews_app.services.service_send_model_event_to_ms_teams import \
                                      ServiceSendModelEventToMsTeams
from binance_ews_app.model.model_binance_article import ModelBinanceArticle
from binance_ews_app.converters.converter_dict_to_binance_article_raw import \
                                               ConverterDictToBinanceArticleRaw
from binance_ews_app.converters.converter_binance_article_to_binance_event import \
                                               ConverterBinanceArticleToBinanceEvent
from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords
from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv


class TestMsTeamsMessagingTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        self.__service_send_binance_event_to_ms_teams       = ServiceSendModelEventToMsTeams()
        self.__converter_dict_to_model_binance_article_raw  = ConverterDictToBinanceArticleRaw()
        self.__converter_model_article_to_model_event       = ConverterBinanceArticleToBinanceEvent()
    
    def test(self):
        raw_data = r'./ews_app\test\data\delisting_event_raw_article_data.json'
        
        parsed_dictionary = open (raw_data, "r")
        article_dict = json.loads(parsed_dictionary.read())
        
        model_raw_article = self.__converter_dict_to_model_binance_article_raw.convert(article_dict=article_dict)
        
        key_article = \
            ModelBinanceArticle(
                                raw_article      = model_raw_article,
                                alert_priority   = EnumPriority.HIGH.name,
                                id               = model_raw_article.id,
                                alert_category   = EnumHighAlertWarningKeyWords.TOKEN_DELISTING,
                                url              = 'https://www.binance.com/en/support/announcement/testing_exmaple'
                                )
        
        model_event_object = \
        self.__converter_model_article_to_model_event.convert(article=key_article,
                                                              trading_affected=False,
                                                              h_spot_tickers=['ALGO/BTC', 'ALICE/BTC', 'ALICE/USDT', \
                                                                      'AMP/USDT', 'ANKR/BTC', 'APE/BTC', 'API3/USDT'],
                                                              important_dates=[1693495466000, 1693495446000, 1693495406000],
                                                              )
        
        self.assertIsNotNone(model_event_object)
        # self.__service_send_binance_event_to_ms_teams.send_message(ms_teams_message=model_event_object.ms_teams_message)