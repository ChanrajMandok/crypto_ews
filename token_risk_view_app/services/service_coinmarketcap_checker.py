import os
import time
import random
import requests

from singleton_decorator import singleton

from token_risk_view_app.services import logger
from token_risk_view_app.decorators.decorator_base_trading_urls import \
                                                       base_trading_urls
from ews_app.model.model_wirex_deposit_currency import ModelWirexDepositCurrency


@singleton
class ServiceCoinMarketCapChecker():

    @base_trading_urls
    def __init__(self,
                 coinmarketcap_ccy_url,
                 coinmarketcap_base_url=None,
                 **kwargs) -> None:
        self.logger_instance = logger
        self.class_name = self.__class__.__name__
        self._coinmarketcap_ccy_url = coinmarketcap_ccy_url


    def token_liquidity_check(self):
            
        timeout = int(os.environ.get('TIMEOUT', 10))
        ssl_verify = False if os.environ.get('SSL_VERIFY', 'True') == "False" else True
        
        session = requests.Session()
        session.verify = ssl_verify
        all_current_tokens = \
            list(set(ModelWirexDepositCurrency.objects.all()))
        
        low_volume_tokens = []
        for token in all_current_tokens:

            url = self._coinmarketcap_ccy_url + token.name + '&start=1&limit=10'
            try:
                response = session.get(url, 
                                    timeout=timeout)
                if response.status_code != 200: 
                    low_volume_tokens.append(token.currency)
                    continue

                json_response = response.json()

                if not "data" in json_response:
                    low_volume_tokens.append(token.currency)
                    continue

                data = json_response['data']

                if not 'marketPairs' in data:
                    low_volume_tokens.append(token.currency)
                    continue

                market_pairs_data = data['marketPairs']

                if not isinstance(market_pairs_data, list) or not market_pairs_data:
                    low_volume_tokens.append(token.currency)
                    continue

                max_volume = None
                for pair_data in market_pairs_data:
                    if 'volumeUsd' in pair_data:
                        if max_volume is None or pair_data['volumeUsd'] > max_volume:
                            max_volume = pair_data['volumeUsd']

                if max_volume is None or max_volume < 5000.0:
                    low_volume_tokens.append(token.currency)

                time.sleep(random.uniform(1, 2))

            except Exception as e:
                self.logger_instance.error(f"Error while fetching data for {token.currency}: {str(e)}")
                low_volume_tokens.append(token.currency)
        
        return low_volume_tokens
