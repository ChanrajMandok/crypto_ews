import os
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency
from ews_app.model.model_wirex_usdm_currency import ModelWirexUsdmCurrency


class TaskPopulateCurrencies():
    
    def __init__(self) -> None:
        self.spot_currencies = os.environ.get('SPOT_CURRENCIES')
        self.usdm_currencies = os.environ.get('USDM_CURRENCIES')
    
    def populate(self):
        spot_ccys = [(i, x) for i, x in enumerate(self.spot_currencies.split(' '))]
        usdm_ccys = [(i, x) for i, x in enumerate(self.usdm_currencies.split(' '))]
        
        try:
            spot_ccy_instances = [ModelWirexSpotCurrency(id=i, currency=x) for i, x in spot_ccys]
            usdm_ccy_instances = [ModelWirexUsdmCurrency(id=i, currency=x) for i, x in usdm_ccys]
        except Exception as e:
            raise Exception(f"Error populating models: {e}")

        try:
            ModelWirexSpotCurrency.objects.bulk_create(spot_ccy_instances, ignore_conflicts=True)
            ModelWirexUsdmCurrency.objects.bulk_create(usdm_ccy_instances, ignore_conflicts=True)
        except Exception as e:
            raise Exception(f"Error populating models: {e}")
