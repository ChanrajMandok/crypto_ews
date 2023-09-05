import json

from django.test import TestCase

from ews_app.enum.enum_priority import EnumPriority
from ews_app.tasks.populate_currencies import TaskPopulateCurrencies
from binance_ews_app.model.model_binance_article import ModelBinanceArticle
from binance_ews_app.services.service_send_binance_event_to_ms_teams import \
                                        ServiceSendModelBinanceEventToMsTeams     
from binance_ews_app.services.service_binance_article_html_retriever import \
                                            ServiceBinanceArticleHtmlRetriever
from binance_ews_app.converters.converter_dict_to_binance_article_raw import \
                                                ConverterDictToBinanceArticleRaw
from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords



class BinanceGalaHardForkReminderTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrencies().populate()
        self.__service_article_html_retriever              = ServiceBinanceArticleHtmlRetriever()
        self.__service_send_binance_event_to_ms_teams      = ServiceSendModelBinanceEventToMsTeams()
        self.__converter_dict_to_model_binance_article_raw = ConverterDictToBinanceArticleRaw()
    
    def test(self):
        filepath = r'./binance_ews_app/test/data/gala_hard_fork_raw_article_data.py'
        f = open (filepath, "r")
        article_dict = json.loads(f.read())
        
        model_raw_article = self.__converter_dict_to_model_binance_article_raw.convert(article_dict=article_dict)
        key_article =\
            ModelBinanceArticle(url              = None,
                                html             = None,
                                id               = model_raw_article.id,
                                raw_article      = model_raw_article,
                                alert_priority   = EnumPriority.HIGH.name,
                                alert_category   = EnumHighAlertWarningKeyWords.CONTRACT_UPGRADE
                                )
    
        model_event_object = self.__service_article_html_retriever.retrieve(articles=[key_article], test=True)
        reminder_msg = model_event_object[0].ms_teams_message
        reminder_msg['title'] = 'REMINDER ' + reminder_msg['title']
        reminder_msg['sections'][1] = {"activityTitle": f"Priority: {EnumPriority.REMINDER.name}"}
        self.__service_send_binance_event_to_ms_teams.send_message(reminder_msg)
        
        
        