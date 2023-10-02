from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from ews_app.service_interfaces.service_db_event_manager_interface import \
                                             ServiceDbEventManagerInterface


@singleton
class ServiceBinanceDbEventManager(ServiceDbEventManagerInterface):

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
        return ModelBinanceEvent
    

    