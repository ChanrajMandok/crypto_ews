from singleton_decorator import singleton

from okx_ews_app.services import logger
from okx_ews_app.model.model_okx_event import \
                                   ModelOkxEvent
from ews_app.service_interfaces.service_db_event_manager_interface \
                                import ServiceDbEventManagerInterface


@singleton
class ServiceOkxDbEventManager(ServiceDbEventManagerInterface):

    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def model_event(self):
        return ModelOkxEvent