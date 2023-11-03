from django.db import transaction
from ews_app.model.model_stablecoin import ModelStableCoin
from ews_app.model.model_spot_currency import ModelSpotCurrency
from ews_app.model.model_usdm_currency import ModelUsdmCurrency


class TaskCleanCurrenciesAndStablecoinsInDb():

    @staticmethod
    @transaction.atomic 
    def clear():
        ModelStableCoin.objects.all().delete()
        ModelSpotCurrency.objects.all().delete()
        ModelUsdmCurrency.objects.all().delete()
        print("Tables cleared successfully!")