import requests
from ews_app.decorators.decorator_webhook_urls import webhooks_urls_required

from ews_app.services import logger
from ews_app.enum.enum_source import EnumSource


class ServiceSendModelEventToMsTeams:
    
    @webhooks_urls_required
    def __init__(self, 
                 cex_webhook,
                 defi_webhook,
                 token_webhook, 
                 stablecoin_webhook,
                 **kwargs
                 ) -> None:
        self.cex_webhook        = cex_webhook
        self.defi_webhook       = defi_webhook 
        self.stablecoin_webhook = stablecoin_webhook
        self.token_webhook      = token_webhook 
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
            if source == EnumSource.BINANCE_ORDERBOOKS.name:
                webhook = self.token_webhook 

            response = requests.post(webhook, json=ms_teams_message, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR {e}") 