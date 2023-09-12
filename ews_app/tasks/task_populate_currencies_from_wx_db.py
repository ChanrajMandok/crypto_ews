from ews_app.services.service_wx_analytics_currencies_retriever import \
                                    ServiceWxAnalyticsCurrenciesRetriever
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency


class TaskpopulateCurrenciesFromWxDb:

    def __init__(self) -> None:
        self.currencies_retriever = ServiceWxAnalyticsCurrenciesRetriever()

    def populate(self):
        currencies = self.currencies_retriever.get_currencies()
        existing_currency_set = set(ModelWirexSpotCurrency.objects.values_list('currency', flat=True))
        new_currencies = [currency for currency in currencies if currency.currency not in existing_currency_set]
        last_id = ModelWirexSpotCurrency.objects.all().order_by('-id').values('id').first()
        
        start_id = last_id['id'] + 1 if last_id else 1

        for index, currency in enumerate(new_currencies):
            currency.id = start_id + index
            
        ModelWirexSpotCurrency.objects.bulk_create(new_currencies)
    