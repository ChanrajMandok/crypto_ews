import os 

from datetime import datetime
from typing import Optional, Union

from binance_ews_app.converters import logger
from ews_app.enum.enum_priority import EnumPriority
from ews_app.model.model_ticker import ModelTicker
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords


class ConverterModelEventToMsTeamsMessage:
    """
    Converts a `ModelBinanceEvent` instance into a Microsoft Teams Message Card format.
    
    The resulting JSON representation of the message card can be used to send messages to a 
    Microsoft Teams channel via a webhook. This converter additionally offers functionalities
    to set the priority of the message based on the `alert_priority` of the event.
    """

    def __init__(self) -> None:
        self.webhook = os.environ.get('WEBHOOK_URL')

    def convert(self,
                url            :str,
                title          :str,
                article_text   :str,
                new_token_issue:bool,
                alert_priority :EnumPriority,
                important_dates:list[datetime],
                networks       :Optional[list[str]],
                alert_category :Union[EnumLowAlertWarningKeyWords,
                                    EnumHighAlertWarningKeyWords],
                h_spot_tickers :Optional[list[ModelTicker]] = None,
                h_usdm_tickers :Optional[list[ModelTicker]] = None,
                l_spot_tickers :Optional[list[ModelTicker]] = None,
                l_usdm_tickers :Optional[list[ModelTicker]] = None) -> dict:
        
        """
        Convert the provided `ModelBinanceEvent` instance into a Microsoft Teams Message Card JSON format.

        The resulting message card includes details like the event title, URL, and associated tickers. It
        also provides actionable buttons based on the event's alert priority.

        Parameters:
        - model_event: Instance detailing a Binance event.

        Returns:
        - A JSON representation of the message card, or None if an error occurs.
        """
        
        url             = url
        title           = title
        article_text    = article_text
        alert_category  = alert_category
        h_spot_tickers  = h_spot_tickers
        h_usdm_tickers  = h_usdm_tickers
        l_spot_tickers  = l_spot_tickers
        l_usdm_tickers  = l_usdm_tickers
        
        formatted_dates = [datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M') \
                           for ts in important_dates] if important_dates else None
        
        dates_str       = ', '.join(formatted_dates) if formatted_dates else None
        network_str     = ', '.join(networks) if networks else None
        msg_title       = f"{alert_category.name} EVENT -  {title}"
        
        try:
                # Create the base Teams message
                message = {
                    "@type": "MessageCard",
                    "@context": "https://schema.org/extensions",
                    "summary": f"Binance {alert_category.value} Event",
                    "themeColor": "FF0000" if alert_priority == EnumPriority.HIGH else "008000",  # Red for HIGH, Yellow for LOW
                    "title": msg_title,
                    "sections": [
                        {
                            "activityTitle": f"URL: {url}",
                        },
                        {
                            "activityTitle": f"Priority: {alert_priority.name}",
                        },
                        {
                            "activityTitle": f"Event Dates: {dates_str}",
                        },

                    ]
                }
                if networks:
                    network = {
                         "activityTitle": f"Network: {network_str}",
                    }
                    message["sections"].append(network)

                if new_token_issue:
                    token_status = {
                        "activityTitle": f"New Token issued: {new_token_issue}",
                    }
                    message["sections"].append(token_status)

                facts = []
                if h_spot_tickers:
                    facts.append({"name": "High Priority Spot Tickers", "value": ", ".join(h_spot_tickers)})
                if h_usdm_tickers:
                    facts.append({"name": "High Priority USDM Tickers", "value": ", ".join(h_usdm_tickers)})
                if l_spot_tickers:
                    facts.append({"name": "Low Priority Spot Tickers", "value": ", ".join(l_spot_tickers)})
                if l_usdm_tickers:
                    facts.append({"name": "Low Priority USDM Tickers", "value": ", ".join(l_usdm_tickers)})

                if facts:
                    ticker_section = {
                        "facts": facts
                    }
                    message["sections"].append(ticker_section)

                return message

        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")

