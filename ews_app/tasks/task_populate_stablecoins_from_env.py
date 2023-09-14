import os

from ews_app.model.model_wirex_stablecoin import ModelWirexStableCoin

class TaskPopulateWirexStableCoinsFromEnv:

    def __init__(self) -> None:
        self.stables = os.environ.get('STABLECOINS')

    def populate(self):

        stablecoin_strings = self.stables.split(' ')
        stablecoins = {(index, currency) for index, currency in enumerate(stablecoin_strings)}
    
        try:
            stablecoin_instances = [ModelWirexStableCoin(id=i, currency=x) for i, x in stablecoins]
        except Exception as e:
            raise Exception(f"Error populating models: {e}")

        try:
            ModelWirexStableCoin.objects.bulk_create(stablecoin_instances, ignore_conflicts=True)
        except Exception as e:
            raise Exception(f"Error populating models: {e}")
        


    