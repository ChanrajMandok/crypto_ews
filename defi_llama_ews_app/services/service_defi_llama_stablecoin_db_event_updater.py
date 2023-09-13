from datetime import datetime

from defi_llama_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from defi_llama_ews_app.store.stores_defi import StoreDefi
from defi_llama_ews_app.model.model_db_defi_last_updated import \
                                           ModelDbDefiLastUpdated
from defi_llama_ews_app.model.model_defi_stablecoin_event import \
                                          ModelDefiStableCoinEvent
from ews_app.services.service_send_model_event_to_ms_teams import \
                                    ServiceSendModelEventToMsTeams
from ews_app.service_interfaces.service_db_event_updater_interface import \
                                             ServiceDbEventUpdaterInterface
from defi_llama_ews_app.services.service_defi_llama_model_stablecoin_retriever \
                                    import ServiceDefiLlamaModelStablecoinRetriever
from defi_llama_ews_app.converters.convert_model_stablecoin_to_model_event import \
                                                  ConvertModelStablecoinToModelEvent


class ServiceDefiLlamaStableCoinDbEventUpdater(ServiceDbEventUpdaterInterface):

    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_send_model_event_to_ms_teams          = ServiceSendModelEventToMsTeams()
        self.converter_model_defi_stablecoin_to_model_event = ConvertModelStablecoinToModelEvent()
        self.service_defi_llama_model_stablecoin_retriever  = ServiceDefiLlamaModelStablecoinRetriever()
        self._store_db_defi_llama_stablecoin_last_updated   = StoreDefi.store_db_defi_stablecoin_llama_last_updated

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def service_send_model_event_to_ms_teams(self):
        return self._service_send_model_event_to_ms_teams

    def store_db_last_updated(self):
        return self._store_db_defi_llama_stablecoin_last_updated 

    def model_db_last_updated(self):
        return ModelDbDefiLastUpdated

    def model_event(self):
        return ModelDefiStableCoinEvent
    
    def service_raw_article_keyword_classifier(self):
        pass
    
    def service_raw_article_retriever(self):
        pass
    
    def service_article_html_retriever(self):
        pass

    def update_db(self):
        try:
            model_stablecoins = self.service_defi_llama_model_stablecoin_retriever.retrieve()

            model_event_objects = \
                [self.converter_model_defi_stablecoin_to_model_event.convert(
                                                        source=EnumSource.DEFI_LLAMA,
                                                        model_stablecoin=x) for x in model_stablecoins]
            
            now = int(datetime.now().timestamp()) * 1000
            # If there are no model event objects, exit early.
            if not model_event_objects:
                ts = self.model_db_last_updated()(last_updated=now)
                self.store_db_last_updated().set(ts)
                return
            
            # Check for duplicates and filter them out using the 'id' field
            existing_ids = self.model_event().objects.filter(id__in=[x.id for x in model_event_objects]).values_list('id', flat=True)
            
            new_events = [event for event in model_event_objects if event.id not in existing_ids]
            
            # Save to DB and send messages for new events
            for event in new_events:
                self._service_send_model_event_to_ms_teams.send_message(event.ms_teams_message)
                event.event_completed = True
                event.save()

            ts = self.model_db_last_updated()(last_updated=now)
            self.store_db_last_updated().set(ts)

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: ERROR - {e}")