import os

from ews_app.model.model_spot_currency import ModelSpotCurrency
from ews_app.model.model_usdm_currency import ModelUsdmCurrency


class TaskPopulateCurrenciesFromEnv():
    
    def __init__(self) -> None:
        self.spot_currencies = os.environ.get('SPOT_CURRENCIES')
        self.usdm_currencies = os.environ.get('USDM_CURRENCIES')
    
    def populate(self):
        spot_tickers = self.spot_currencies.split(' ')
        usdm_tickers = self.usdm_currencies.split(' ')
        
        spot_currencies = set()
        for pair in spot_tickers:
            spot_currencies.update(pair.split('/'))

        # Enumerate the unique currencies and assign an index
        spot_ccys = {(index, currency) for index, currency in enumerate(sorted(spot_currencies))}
        
        usdm_currencies = set()
        for pair in usdm_tickers:
            usdm_currencies.update(pair.split('-'))

        usdm_ccys = {(index, currency) for index, currency in enumerate(sorted(usdm_currencies))}
                
        try:
            spot_ccy_instances = [ModelSpotCurrency(id=i, currency=x) for i, x in spot_ccys]
            usdm_ccy_instances = [ModelUsdmCurrency(id=i, currency=x) for i, x in usdm_ccys]
        except Exception as e:
            raise Exception(f"Error populating models: {e}")

        try:
            ModelSpotCurrency.objects.bulk_create(spot_ccy_instances, ignore_conflicts=True)
            ModelUsdmCurrency.objects.bulk_create(usdm_ccy_instances, ignore_conflicts=True)
        except Exception as e:
            raise Exception(f"Error populating models: {e}")
