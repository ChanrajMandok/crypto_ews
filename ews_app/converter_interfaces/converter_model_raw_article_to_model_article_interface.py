import abc

from typing import Union

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords


class ConverterModelRawArticleToModelArticleInterface(metaclass=abc.ABCMeta):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def model_article_raw(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def model_article(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    def __init__(self) -> None:
        super().__init__()

    def convert(self, 
            alert_priority: EnumPriority,
            model_raw_article: model_article_raw,
            alert_category: Union[EnumLowAlertWarningKeyWords, 
                                    EnumHighAlertWarningKeyWords]) -> model_article:

        try:
            article_object = self.model_article()(
                                                  alert_category=alert_category, 
                                                  alert_priority=alert_priority,
                                                  raw_article=model_raw_article, 
                                                  id=model_raw_article.id)
            
            return article_object

        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")
            return None