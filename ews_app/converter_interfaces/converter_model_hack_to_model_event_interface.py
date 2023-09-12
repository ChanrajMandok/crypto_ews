import abc

from typing import Optional, List

from ews_app.enum.enum_source import EnumSource
from defi_ews_app.model.model_defi_llama_hack import ModelDefiLlamaHack
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.converters.converter_model_event_to_ms_teams_message \
                         import ConverterModelEventToMsTeamsMessage


class ConverterModelHackToModelEventInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def class_name(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def model_hack(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def model_event(self):
        raise NotImplementedError   
    
    def __init__(self) -> None:
        self._converter_model_event_to_ms_teams_message = \
                        ConverterModelEventToMsTeamsMessage()

    def convert(self,
                source          : EnumSource,
                model_hack      : ModelDefiLlamaHack,  
                h_spot_tickers  : Optional[List[str]] = [],
                h_usdm_tickers  : Optional[List[str]] = [],
                l_spot_tickers  : Optional[List[str]] = [],
                l_usdm_tickers  : Optional[List[str]] = []):
        """
        Abstract method to convert an article model into an event model.
        """

        try:

            exploit          = model_hack.exploit
            protocol         = model_hack.protocol        
            blockchain       = model_hack.blockchain
            release_date     = model_hack.release_date
            alert_priority   = model_hack.alert_priority
            
            if not blockchain:
                title = f"{protocol} Protocol, Exploit: {exploit}"
            else:
                blockchain_str = ', '.join(blockchain).replace(', ', ' & ')
                network_label = 'Networks' if len(blockchain) > 1 else 'Network'
                title = f"{protocol} Protocol, {blockchain_str} {network_label}"

            title            = title  
            url              = model_hack.url
            important_dates  = [release_date]
            network_tokens   = model_hack.network_tokens
            trading_affected = model_hack.trading_affected
            alert_category   = EnumHighAlertWarningKeyWords.HACK
            hacked_amount    = model_hack.hacked_amount_m if model_hack.hacked_amount_m is not None else 25  

            id = int(release_date)/int(round(hacked_amount, ndigits=0)+100000)
            
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
                    id                = int(id),
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

    