import os
import abc

from datetime import datetime

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.model_interfaces.model_article_interface import \
                                         ModelArticleInterface
from ews_app.model_interfaces.model_article_raw_interface import \
                                          ModelArticleRawInterface
from ews_app.enum.enum_false_altert_phrases import EnumFalseAlertPhrases


class ServiceBinanceRawArticleKeywordClassifierInterface(metaclass=abc.ABCMeta):
    """
    Services Searches Titles of News Dict (Catalogs) for Keywords and ensures the Events 
    are within a lookback window
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'classify_articles') and
                callable(subclass.classify_articles))

    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError

    @abc.abstractmethod
    def converter_ra_to_a(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def store(self):
        raise NotImplementedError   
    
    def __init__(self) -> None:
        self.__refresh_increment_mins = int(os.environ.get('UPDATE_REFRESH_INCREMENT_MINS', 15))
        self.__lookback_days          = int(os.environ.get('RELEVENT_NEWS_LOOKBACK_DAYS', 30))
        self.__max_lookback_time      = self.__lookback_days * 24 * 60 * 60 * 1000
        self.__false_alert_phrases    = {phrase.value.lower() for phrase in EnumFalseAlertPhrases}
        self.__low_priority_keywords  = {keyword.value.lower() for keyword in EnumLowAlertWarningKeyWords}
        self.__high_priority_keywords = {keyword.value.lower() for keyword in EnumHighAlertWarningKeyWords}

    def classify_articles(self, raw_articles: list[ModelArticleRawInterface]) -> list[ModelArticleInterface]:
        
        relevant_articles = []
        current_ts = int(datetime.utcnow().timestamp() * 1000)
        
        last_update = self.store().get()

        for model_raw_article_object in raw_articles:
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
                priority = EnumPriority.LOW.name
                keyword_found = EnumHighAlertWarningKeyWords(list(intersected_keywords)[0])
            else:
                intersected_keywords = title_words & self.__low_priority_keywords
                if intersected_keywords:
                    priority = EnumPriority.LOW.name
                    keyword_found = EnumLowAlertWarningKeyWords(list(intersected_keywords)[0])
                else:
                    continue

            article_model = self.converter_ra_to_a().convert(alert_priority=priority,
                                                             alert_category=keyword_found,
                                                             model_raw_article=model_raw_article_object)

            relevant_articles.append(article_model)

        return relevant_articles

    def _contains_false_alert(self, title_words:str):
        return self.__false_alert_phrases & title_words