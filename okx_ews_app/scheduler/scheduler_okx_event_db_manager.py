import os

from singleton_decorator import singleton

from okx_ews_app.scheduler        import logger
from okx_ews_app.services.service_okx_db_event_manager \
                          import ServiceOkxDbEventManager
from ews_app.scheduler_interfaces.scheduler_db_event_manager_interface \
                                 import SchedularDbEventManagerInterface


@singleton
class SchedularOkxEventDbManager(SchedularDbEventManagerInterface):
    
    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._refresh_increment_mins = int(os.environ.get('MANAGER_REFRESH_INCREMENT_MINS',10))
        self._service_okx_db_event_manager = ServiceOkxDbEventManager()

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

    def service_db_event_manager(self):
        return self._service_okx_db_event_manager