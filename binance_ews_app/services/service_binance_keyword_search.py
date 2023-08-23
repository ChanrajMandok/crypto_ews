import os
from datetime import datetime

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_false_altert_phrases import EnumFalseAlertPhrases
from binance_ews_app.model.model_binance_article_raw import ModelBinanceArticleRaw
from ews_app.enum.enum_low_alert_warning_key_words import EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords
from binance_ews_app.converters.converter_model_raw_article_to_model_article import ConverterModelRawArticleToModelBinanceArticle


class ServiceBinanceKeywordSearch:
    """
    Services Searches Titles of News Dict (Catalogs) for Keywords and ensures the Events are 
    within a lookback window of 30 days 
    """
    
    def __init__(self) -> None:
        self.lookback_days                      = int(os.environ.get('RELEVENT_NEWS_LOOKBACK_DAYS', 30))
        self.max_lookback_time                  = self.lookback_days * 24 * 60 * 60 * 1000
        self.converter_a_to_ma                  = ConverterModelRawArticleToModelBinanceArticle()
        self.false_alert_phrases                = {phrase.name.lower() for phrase in EnumFalseAlertPhrases}
        self.low_priority_keywords              = {keyword.name.lower() for keyword in EnumLowAlertWarningKeyWords}
        self.high_priority_keywords             = {keyword.name.lower() for keyword in EnumHighAlertWarningKeyWords}

    def _contains_false_alert(self, title_words):
        return self.false_alert_phrases & title_words

    def search_articles(self, articles: list[ModelBinanceArticleRaw]) -> list[dict]:
        
        relevant_articles = []
        current_ts = int(datetime.utcnow().timestamp() * 1000)
        
        for model_raw_article_object in articles:
            if not isinstance(model_raw_article_object, ModelBinanceArticleRaw):
                continue

            # model object negates need to check type/ Null status
            title = model_raw_article_object.title.lower()
            title_words = set(title.split())

            # False alert check, if false alert skip value in loop
            if self._contains_false_alert(title_words):
                continue

            # Time check, if not in allowable timeframe, skip in loop
            ts = model_raw_article_object.release_date
            if current_ts - ts > self.max_lookback_time:
                continue

            # High priority check
            intersected_keywords = title_words & self.high_priority_keywords
            if intersected_keywords:
                priority = EnumPriority.HIGH
                keyword_found = list(intersected_keywords)[0]
            else:
                intersected_keywords = title_words & self.low_priority_keywords
                if intersected_keywords:
                    priority = EnumPriority.LOW
                    keyword_found = list(intersected_keywords)[0]
                else:
                    continue

            article_model = self.converter_a_to_ma.convert(alert_priority=priority,
                                                           alert_category=keyword_found.upper(),
                                                           model_raw_article=model_raw_article_object)

            relevant_articles.append(article_model)


        return relevant_articles

