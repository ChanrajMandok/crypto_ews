import abc

from decimal import Decimal
from datetime import datetime
from typing import Union, Optional

from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.converters.converter_model_event_to_ms_teams_message import \
                                       ConverterModelEventToMsTeamsMessage
                                       
                                       
class ConverterDictToModelTokenVolatilityEventInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    

    @abc.abstractmethod
    def model_event(self):
        raise NotImplementedError   
    
    def __init__(self) -> None:
        self._converter_model_event_to_ms_teams_message = \
                        ConverterModelEventToMsTeamsMessage()
                        
    def convert(self,
                url: str,
                title: str,
                release_date: int, 
                important_dates : list[datetime],
                increment_in_seconds: int,
                alert_category:Union[EnumLowAlertWarningKeyWords, 
                                      EnumHighAlertWarningKeyWords],
                network_tokens  : Optional[list[str]] = None,
                h_spot_tickers  : Optional[list[str]] = None,
                h_usdm_tickers  : Optional[list[str]] = None,
                l_spot_tickers  : Optional[list[str]] = None,
                l_usdm_tickers  : Optional[list[str]] = None
                ):
        """
        Abstract method to convert an article model into an event model.
        """
        source = EnumSource.BINANCE_ORDERBOOKS
        trading_affected = False
        alert_priority = EnumPriority.HIGH.name
        
        id = int(release_date/increment_in_seconds)
        
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

