from typing import Optional
from datetime import datetime

from binance_ews_app.converters import logger
from binance_ews_app.model.model_binance_event import \
                                       ModelBinanceEvent
from binance_ews_app.model.model_binance_article import \
                                      ModelBinanceArticle
from binance_ews_app.converters.converter_model_event_to_ms_teams_message \
                                 import ConverterModelEventToMsTeamsMessage


class ConverterModelArticleToModelEvent:
    
    """
    Responsible for converting an instance of `ModelBinanceArticle` into 
    an instance of `ModelBinanceEvent`.
    """
    def __init__(self) -> None:
        self.converter_model_event_to_ms_teams_message = \
                      ConverterModelEventToMsTeamsMessage()

    def convert(self,
                trading_affected : bool,
                important_dates : list[datetime],
                article         : ModelBinanceArticle,
                network_tokens  : Optional[list[str]] = None,
                h_spot_tickers  : Optional[list[str]] = None,
                h_usdm_tickers  : Optional[list[str]] = None,
                l_spot_tickers  : Optional[list[str]] = None,
                l_usdm_tickers  : Optional[list[str]] = None):
    
        
        """
        Convert a ModelBinanceArticle instance to a ModelBinanceEvent
        instance.

        Utilizes data from the given `ModelBinanceArticle` and combines 
        it with additional provided parameters to create a `ModelBinanceEvent`
        instance. If any issues arise during the conversion, errors are logged.

        Parameters:
        - article: The ModelBinanceArticle instance to convert.
        - release_date, code, title, spot_pairs, usdm_pairs, 
        important_dates: Additional data 
          for the ModelBinanceEvent instance.

        Returns:
        - A new ModelBinanceEvent instance.
        
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
                self.converter_model_event_to_ms_teams_message.convert(
                    url                = url,
                    title              = title,
                    network_tokens      = network_tokens,
                    alert_priority     = alert_priority,
                    alert_category     = alert_category,
                    h_spot_tickers     = h_spot_tickers,
                    h_usdm_tickers     = h_usdm_tickers,
                    l_spot_tickers     = l_spot_tickers,
                    l_usdm_tickers     = l_usdm_tickers,
                    trading_affected    = trading_affected, 
                    important_dates    = sorted(important_dates,reverse=True)
                )

            event = ModelBinanceEvent(
                    release_date      = release_date,
                    id                = id,
                    url               = url,
                    title             = title,
                    network_tokens     = network_tokens,
                    ms_teams_message  = teams_message,
                    l_spot_tickers    = l_spot_tickers,
                    h_usdm_tickers    = h_usdm_tickers,
                    l_usdm_tickers    = l_usdm_tickers,
                    alert_priority    = alert_priority,
                    h_spot_tickers    = h_spot_tickers,
                    alert_category    = alert_category,
                    important_dates   = important_dates,
                    trading_affected = trading_affected,
                                      )
            
            return event
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")
