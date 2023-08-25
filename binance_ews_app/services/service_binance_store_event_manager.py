from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from binance_ews_app.services import logger



class ServiceBinanceStoreEventManager:
    
    def update(self, instances : list[ModelBinanceEvent]):
        pass
    
    ## to manage and remove values from the store when the timestamps expire