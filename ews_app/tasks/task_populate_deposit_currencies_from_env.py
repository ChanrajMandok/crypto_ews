from ews_app.decorators.decorator_deposit_currencies import \
                                     wirex_deposit_currencies
from ews_app.model.model_wirex_deposit_currency import ModelWirexDepositCurrency


class TaskpopulateDepositCurrenciesFromEnv:

    @wirex_deposit_currencies
    def __init__(self,
                 ccy_namee_dict) -> None:
        self._ccy_namee_dict = ccy_namee_dict,

    def populate(self):
        currencies_raw = self._ccy_namee_dict[0]
        
        currencies = [ModelWirexDepositCurrency(id=i, currency=x, name=currencies_raw[x]) for i,x in list(enumerate(currencies_raw.keys()))]

        existing_currency_set = set(ModelWirexDepositCurrency.objects.values_list('currency', flat=True))
        new_currencies = [currency for currency in currencies if currency.currency not in existing_currency_set]
        last_id = ModelWirexDepositCurrency.objects.all().order_by('-id').values('id').first()
        
        start_id = last_id['id'] + 1 if last_id else 1

        for index, currency in enumerate(new_currencies):
            currency.id = start_id + index
            currency.name = currency.name.lower().replace(" ", "-")
            
        ModelWirexDepositCurrency.objects.bulk_create(new_currencies)