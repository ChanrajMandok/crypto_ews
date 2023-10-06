from singleton_decorator import singleton

from defi_llama_ews_app.scheduler import logger
from ews_app.decorators.decorator_refresh_increments import \
                                 decorator_refresh_increments
from ews_app.scheduler_interfaces.scheduler_db_event_updater_interface import \
                                               SchedularDbEventUpdaterInterface
from defi_llama_ews_app.services.service_defi_llama_bridge_hack_db_event_updater import \
                                                 ServiceDefiLlamaBridgeHackDbEventUpdater


@singleton
class SchedularDefiLlamaBridgeHackEventDbUpdater(SchedularDbEventUpdaterInterface):
    
    @decorator_refresh_increments
    def __init__(self, 
                 defi_llama_refresh_increment_mins,
                 **kwargs) -> None:
        super().__init__()
        self._logger_instance = logger
        self._refresh_increment_mins = defi_llama_refresh_increment_mins
        self._service_defi_llama_bridge_hack_db_event_updater = ServiceDefiLlamaBridgeHackDbEventUpdater()

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

    def service_db_event_updater(self):
        return self._service_defi_llama_bridge_hack_db_event_updater