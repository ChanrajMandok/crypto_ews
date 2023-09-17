import os
import requests

from ews_app.services import logger

from ews_app.enum.enum_source import EnumSource


class ServiceSendModelEventToMsTeams:

    def __init__(self) -> None:
        self.cex_webhook        = os.environ.get('CEX_WEBHOOK')
        self.defi_webhook       = os.environ.get('DEFI_WEBHOOK')
        self.stablecoin_webhook = os.environ.get('STABELCOIN_WEBHOOK')
        self.headers            = {'Content-Type': 'application/json'}

    def send_message(self,
                     source: EnumSource,
                     ms_teams_message: dict) -> None:
        try:

            if source == EnumSource.BINANCE.name or source == EnumSource.OKX.name:
                webhook = self.cex_webhook
            if source == EnumSource.DEFI_LLAMA.name:
                webhook = self.defi_webhook
            if source == EnumSource.DEFI_LLAMA_STABLECOINS.name:
                webhook = self.stablecoin_webhook

            response = requests.post(webhook, json=ms_teams_message, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR {e}") 