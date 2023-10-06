import os

from singleton_decorator import singleton

from okx_ews_app.scheduler import logger
from okx_ews_app.services.service_okx_db_event_updater import \
                                        ServiceOkxDbEventUpdater
from ews_app.scheduler_interfaces.scheduler_db_event_updater_interface \
                                 import SchedularDbEventUpdaterInterface


@singleton
class SchedularOkxEventDbUpdater(SchedularDbEventUpdaterInterface):
    
    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_okx_db_event_updater = ServiceOkxDbEventUpdater()
        self._refresh_increment_mins = int(os.environ.get('UPDATE_REFRESH_INCREMENT_MINS',10))

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
        return self._service_okx_db_event_updater