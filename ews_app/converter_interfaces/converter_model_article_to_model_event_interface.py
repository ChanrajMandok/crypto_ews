import abc

from datetime import datetime
from typing import Optional, List, Union

from ews_app.enum.enum_source import EnumSource
from binance_ews_app.model.model_binance_article import \
                                        ModelBinanceArticle
from okx_ews_app.model.model_okx_article import ModelOkxArticle
from ews_app.converters.converter_model_event_to_ms_teams_message \
                         import ConverterModelEventToMsTeamsMessage


class ConverterArticleToEventInterface(metaclass=abc.ABCMeta):
    """
    Abstract Base Class that serves as a blueprint for classes that convert 
    different article models into event models.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def model_event(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def class_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def logger_instance(self):
        raise NotImplementedError
    
    def __init__(self) -> None:
        self._converter_model_event_to_ms_teams_message = \
                        ConverterModelEventToMsTeamsMessage()

    def convert(self,
                trading_affected: bool,
                source          : EnumSource,
                important_dates : List[datetime],
                article         : Union[ModelBinanceArticle, ModelOkxArticle],  
                network_tokens  : Optional[list[str]] = None,
                h_spot_tickers  : Optional[List[str]] = None,
                h_usdm_tickers  : Optional[List[str]] = None,
                l_spot_tickers  : Optional[List[str]] = None,
                l_usdm_tickers  : Optional[List[str]] = None):
        """
        Abstract method to convert an article model into an event model.
        """

        try:
            raw_article    = article.raw_article

            id             = article.id
            url            = article.url
            title          = raw_article.title  
            alert_priority = article.alert_priority
            alert_category = article.alert_category
            release_date   = raw_article.release_date
            
            teams_message = \
                self._converter_model_event_to_ms_teams_message.convert(
                    url                = url,
                    title              = title,
                    source             = source,
                    network_tokens     = network_tokens,
                    alert_priority     = alert_priority,
                    alert_category     = alert_category,
                    h_spot_tickers     = h_spot_tickers,
                    h_usdm_tickers     = h_usdm_tickers,
                    l_spot_tickers     = l_spot_tickers,
                    l_usdm_tickers     = l_usdm_tickers,
                    trading_affected   = trading_affected, 
                    important_dates    = sorted(important_dates,reverse=True)
                )

            event = self.model_event()(
                    release_date      = release_date,
                    id                = id,
                    url               = url,
                    title             = title,
                    source            = source.name,
                    network_tokens    = network_tokens,
                    ms_teams_message  = teams_message,
                    l_spot_tickers    = l_spot_tickers,
                    h_usdm_tickers    = h_usdm_tickers,
                    l_usdm_tickers    = l_usdm_tickers,
                    alert_priority    = alert_priority,
                    h_spot_tickers    = h_spot_tickers,
                    alert_category    = alert_category,
                    important_dates   = important_dates,
                    trading_affected  = trading_affected,
                                      )
            
            return event
        
        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")
