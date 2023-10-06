from singleton_decorator import singleton

from token_risk_view_app.services import logger
from ews_app.decorators.decorator_refresh_increments import \
                                 decorator_refresh_increments
from token_risk_view_app.observers.observer_store_token_price_change import \
                                                ObserverStoreTokenPriceChange
from ews_app.scheduler_interfaces.scheduler_store_event_updater_interface import \
                                               SchedularStoreEventUpdaterInterface
from token_risk_view_app.services.service_token_risk_view_app_store_event_updater import \
                                                                  ServiceStoreEventUpdater


@singleton
class SchedulerTokenPriceChangeStoreUpdater(SchedularStoreEventUpdaterInterface):
    
    @decorator_refresh_increments
    def __init__(self,
                 orderbooks_refresh_increment_mins,
                 *args,
                 **kwargs) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_store_event_updater = ServiceStoreEventUpdater()
        self._observer_store_token_price_change = ObserverStoreTokenPriceChange()
        self._refresh_increment_mins = orderbooks_refresh_increment_mins
        
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def max_instances(self):
        return int(1)
    
    @property
    def refresh_increment_mins(self):
        return self._refresh_increment_mins

    def service_store_event_updater(self):
        return self._service_store_event_updater 
    
    def observer(self):
        return self._observer_store_token_price_change