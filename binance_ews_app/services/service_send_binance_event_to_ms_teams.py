import os
import json
import requests

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_event import ModelBinanceEvent


class ServiceSendModelBinanceEventToMsTeams:

    def __init__(self) -> None:
        self.webhook = os.environ.get('WEBHOOK_URL')
        self.headers = {'Content-Type': 'application/json'}

    def send_message(self, ms_teams_message: dict) -> None:
        try:
            # Validate JSON format
            json_str = json.dumps(ms_teams_message)
            if len(json_str) > 28 * 1024:  # 28 KB
                logger.error("The payload size exceeds 28 KB limit.")
                return

            response = requests.post(self.webhook, json=ms_teams_message, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR {e}")