from typing import Optional
from datetime import datetime

from binance_ews_app.converters import logger
from ews_app.model.model_ticker import ModelTicker
from binance_ews_app.model.model_binance_event import \
                                         ModelBinanceEvent
from binance_ews_app.model.model_binance_article import \
                                       ModelBinanceArticle


class ConverterModelArticleToModelEvent:
    
    def convert(self,
                article_text: str,
                article: ModelBinanceArticle,
                important_dates: list[datetime],
                networks: Optional[list[str]] = None,
                h_spot_tickers: Optional[list[ModelTicker]] = None,
                h_usdm_tickers: Optional[list[ModelTicker]] = None,
                l_spot_tickers: Optional[list[ModelTicker]] = None,
                l_usdm_tickers: Optional[list[ModelTicker]] = None):
    
        
        """
        Convert a ModelBinanceArticle instance to a ModelBinanceEvent
        instance.

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
            release_date   = raw_article.release_date
            title          = raw_article.title  
            url            = article.url
            id             = article.id
            alert_priority = article.alert_priority
            alert_category = article.alert_category
            

            event = ModelBinanceEvent(
                    release_date      = release_date,
                    url               = url,
                    title             = title,
                    article_text      = article_text,
                    id                = id,
                    networks          = networks,
                    alert_priority    = alert_priority,
                    important_dates   = important_dates,
                    alert_category    = alert_category,
                    h_spot_tickers    = h_spot_tickers,
                    h_usdm_tickers    = h_usdm_tickers,
                    l_spot_tickers    = l_spot_tickers,
                    l_usdm_tickers    = l_usdm_tickers,
                                      )
            
            return event
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")
