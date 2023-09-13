import os

from singleton_decorator import singleton

from defi_llama_ews_app.scheduler import logger
from defi_llama_ews_app.services.service_defi_llama_hack_db_event_updater import \
                                              ServiceDefiLlamaHackDbEventUpdater
from ews_app.scheduler_interfaces.scheduler_db_event_updater_interface \
                                 import SchedularDbEventUpdaterInterface


@singleton
class SchedularDefiLlamaEventDbUpdater(SchedularDbEventUpdaterInterface):
    
    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_defi_llama_db_event_updater = ServiceDefiLlamaHackDbEventUpdater()
        self._refresh_increment_mins = int(os.environ.get('DEFI_LLAMA_UPDATE_REFRESH_INCREMENT_MINS',3))

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
        return self._service_defi_llama_db_event_updater 