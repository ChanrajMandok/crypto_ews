import os
from datetime import datetime

from binance_ews_app.store.stores_binance import\
                                    StoresBinance
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_false_altert_phrases import \
                                 EnumFalseAlertPhrases
from binance_ews_app.model.model_binance_article import \
                                       ModelBinanceArticle
from ews_app.enum.enum_low_alert_warning_key_words import \
                                 EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                  EnumHighAlertWarningKeyWords                            
from binance_ews_app.model.model_binance_article_raw import \
                                        ModelBinanceArticleRaw                                                                
from binance_ews_app.converters.converter_model_raw_article_to_model_article import \
                                                ConverterModelRawArticleToModelArticle


class ServiceBinanceRawArticleKeywordClassifier:
    """
    Services Searches Titles of News Dict (Catalogs) for Keywords and ensures the Events 
    are within a lookback window of 30 days 
    """
    
    def __init__(self) -> None:
        self.__refresh_increment_mins = int(os.environ.get('REFRESH_INCREMENT_MINS', 5))
        self.__lookback_days          = int(os.environ.get('RELEVENT_NEWS_LOOKBACK_DAYS', 60))
        self.__binance_event_store    = StoresBinance.store_binance_events
        self.__converter_a_to_ma      = ConverterModelRawArticleToModelArticle()
        self.__max_lookback_time      = self.__lookback_days * 24 * 60 * 60 * 1000
        self.__false_alert_phrases    = {phrase.name.lower() for phrase in EnumFalseAlertPhrases}
        self.__low_priority_keywords  = {keyword.name.lower() for keyword in EnumLowAlertWarningKeyWords}
        self.__high_priority_keywords = {keyword.name.lower() for keyword in EnumHighAlertWarningKeyWords}


    def classify_articles(self, raw_articles: list[ModelBinanceArticleRaw]) -> list[ModelBinanceArticle]:
        
        relevant_articles = []
        current_ts = int(datetime.utcnow().timestamp() * 1000)
        
        last_update = self.__binance_event_store.get_last_updated_ts()

        for model_raw_article_object in raw_articles:
            if not isinstance(model_raw_article_object, ModelBinanceArticleRaw):
                continue

            # Time check, if not in allowable timeframe, skip in loop
            ts = model_raw_article_object.release_date
            if last_update:
                if current_ts - ts > self.__refresh_increment_mins*60*1000:
                    continue
            else:
                if current_ts - ts > self.__max_lookback_time:
                    continue

            # model object negates need to check type/ Null status
            title = model_raw_article_object.title.lower()
            title_words = set(title.split())

            # False alert check, if false alert skip value in loop
            if self._contains_false_alert(title_words):
                continue

            # High priority check
            intersected_keywords = title_words & self.__high_priority_keywords
            if intersected_keywords:
                priority = EnumPriority.HIGH
                keyword_found = EnumHighAlertWarningKeyWords(list(intersected_keywords)[0])
            else:
                intersected_keywords = title_words & self.__low_priority_keywords
                if intersected_keywords:
                    priority = EnumPriority.LOW
                    keyword_found = EnumLowAlertWarningKeyWords(list(intersected_keywords)[0])
                else:
                    continue

            article_model = self.__converter_a_to_ma.convert(alert_priority=priority,
                                                             alert_category=keyword_found,
                                                             model_raw_article=model_raw_article_object)

            relevant_articles.append(article_model)

        return relevant_articles

    def _contains_false_alert(self, title_words:str):
        return self.__false_alert_phrases & title_words