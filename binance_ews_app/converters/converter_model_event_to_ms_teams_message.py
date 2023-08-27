import os 
import json

from binance_ews_app.converters import logger
from ews_app.enum.enum_priority import EnumPriority
from binance_ews_app.model.model_binance_event import ModelBinanceEvent


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
                model_event: ModelBinanceEvent) -> json:
        
        """
        Convert the provided `ModelBinanceEvent` instance into a Microsoft Teams Message Card JSON format.

        The resulting message card includes details like the event title, URL, and associated tickers. It
        also provides actionable buttons based on the event's alert priority.

        Parameters:
        - model_event: Instance detailing a Binance event.

        Returns:
        - A JSON representation of the message card, or None if an error occurs.
        """
        
        try:    
            url             = model_event.url
            title           = model_event.title
            alert_category  = model_event.alert_category
            h_spot_tickers  = model_event.h_spot_tickers
            h_usdm_tickers  = model_event.h_usdm_tickers
            l_spot_tickers  = model_event.l_spot_tickers
            l_usdm_tickers  = model_event.l_usdm_tickers
            alert_level     = model_event.alert_priority
            msg_title = f"[{alert_category.value}]{title}"
            
            # Constructing the list of tickers with required formatting
            h_spot_tickers_str = "**" + "**, **".join(h_spot_tickers) + "**" if h_spot_tickers else ""
            h_usdm_tickers_str = "**" + "**, **".join(h_usdm_tickers) + "**" if h_usdm_tickers else ""

            l_spot_tickers_str = ", ".join(l_spot_tickers) if l_spot_tickers else ""
            l_usdm_tickers_str = ", ".join(l_usdm_tickers) if l_usdm_tickers else ""

            ticker_sections = []
            if h_spot_tickers_str:
                ticker_sections.append({"startGroup": True, "text": f"High Priority Spot Tickers: {h_spot_tickers_str}"})
            if h_usdm_tickers_str:
                ticker_sections.append({"startGroup": True, "text": f"High Priority USDM Tickers: {h_usdm_tickers_str}"})
            if l_spot_tickers_str:
                ticker_sections.append({"startGroup": True, "text": f"Low Priority Spot Tickers: {l_spot_tickers_str}"})
            if l_usdm_tickers_str:
                ticker_sections.append({"startGroup": True, "text": f"Low Priority USDM Tickers: {l_usdm_tickers_str}"})

            card = {
                "@context": "https://schema.org/extensions",
                "@type": "MessageCard",
                "title": msg_title,
                "sections": [
                    {
                        "startGroup": True,
                        "activitySubtitle": f"## URL:{url}",
                    }
                ] + ticker_sections  # Append the ticker sections after the URL section
            }

            # Adding alert levels based on `alert_priority`
            if alert_level == EnumPriority.HIGH.value:
                card["potentialAction"] = [
                    {
                        "@type": "OpenUri",
                        "name": "Set as Urgent",
                        "targets": [{"os": "default", "uri": f"{self.webhook}?setUrgent=true"}]
                    }
                ]

            elif alert_level == EnumPriority.LOW.value:
                card["potentialAction"] = [
                    {
                        "@type": "OpenUri",
                        "name": "Set as Important",
                        "targets": [{"os": "default", "uri": f"{self.webhook}?setImportant=true"}]
                    }
                ]
            
            return json.dumps(card, indent=4)

        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")