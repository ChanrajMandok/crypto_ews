from typing import Optional

from ews_app.enum.enum_source import EnumSource
from defi_llama_ews_app.converters import logger
from ews_app.enum.enum_priority import EnumPriority
from defi_llama_ews_app.model.model_defi_stablecoin_event import \
                                          ModelDefiStableCoinEvent
from ews_app.converters.converter_model_event_to_ms_teams_message import \
                                       ConverterModelEventToMsTeamsMessage
from defi_llama_ews_app.model.model_defi_stablecoin import ModelDefiStablecoin


class ConvertModelStablecoinToModelEvent():

    def __init__(self) -> None:
        self.logger_instance = logger
        self.class_name = self.__class__.__name__
        self._converter_model_event_to_ms_teams_message = \
                        ConverterModelEventToMsTeamsMessage()

    def convert(self,
                source          : EnumSource,
                model_stablecoin: ModelDefiStablecoin,  
                h_spot_tickers  : Optional[list[str]] = [],
                h_usdm_tickers  : Optional[list[str]] = [],
                l_spot_tickers  : Optional[list[str]] = [],
                l_usdm_tickers  : Optional[list[str]] = []):
        """
        Abstract method to convert an article model into an event model.
        """

        try:
            url              = model_stablecoin.url
            alert_priority   = EnumPriority.HIGH.name
            release_date     = model_stablecoin.release_date
            alert_category   = model_stablecoin.alert_category
            trading_affected = model_stablecoin.trading_affected
            stablecoin       = model_stablecoin.stablecoin.currency
            price            = model_stablecoin.price
            network_tokens   = [stablecoin]

            important_dates  = [release_date]
            title            = f"{stablecoin} {alert_category.name.title()}: Price ${price}"

            id = int(release_date)/(int(model_stablecoin.stablecoin.id)+10000)
  
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

            event = ModelDefiStableCoinEvent(
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

    