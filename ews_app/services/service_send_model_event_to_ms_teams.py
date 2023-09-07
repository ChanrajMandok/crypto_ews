import os
import requests

from ews_app.services import logger


class ServiceSendModelEventToMsTeams:

    def __init__(self) -> None:
        self.webhook = os.environ.get('WEBHOOK_URL')
        self.headers = {'Content-Type': 'application/json'}

    def send_message(self, ms_teams_message: dict) -> None:
        try:

            response = requests.post(self.webhook, json=ms_teams_message, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR {e}")