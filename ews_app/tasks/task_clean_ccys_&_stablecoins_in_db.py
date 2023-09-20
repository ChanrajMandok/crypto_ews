from django.db import transaction

from ews_app.model.model_wirex_stablecoin import ModelWirexStableCoin
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency
from ews_app.model.model_wirex_usdm_currency import ModelWirexUsdmCurrency


class TaskCleanCurrenciesAndStablecoinsInDb():

    @staticmethod
    @transaction.atomic 
    def clear():
        ModelWirexStableCoin.objects.all().delete()
        ModelWirexSpotCurrency.objects.all().delete()
        ModelWirexUsdmCurrency.objects.all().delete()
        print("Tables cleared successfully!")