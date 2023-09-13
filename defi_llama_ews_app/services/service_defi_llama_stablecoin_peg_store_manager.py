from defi_llama_ews_app.services import logger
from defi_llama_ews_app.model.model_defi_stablecoin_event import \
                                            ModelDefiStableCoinEvent
from ews_app.service_interfaces.service_db_event_manager_interface \
                                import ServiceDbEventManagerInterface

class ServiceDefiLlamaStablecoinPegStoreManager(ServiceDbEventManagerInterface):

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
        return ModelDefiStableCoinEvent