import os
import re

from datetime import datetime
from typing_extensions import override
from singleton_decorator import singleton

from django.db import transaction
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
from defi_llama_ews_app.converters.convert_model_stablecoin_to_model_event import \
                                                 ConvertModelStablecoinToModelEvent
from defi_llama_ews_app.services.service_defi_llama_model_stablecoin_retriever import \
                                               ServiceDefiLlamaModelStablecoinRetriever


@singleton
class ServiceDefiLlamaStableCoinDbEventUpdater(ServiceDbEventUpdaterInterface):

    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_send_model_event_to_ms_teams          = ServiceSendModelEventToMsTeams()
        self.converter_model_defi_stablecoin_to_model_event = ConvertModelStablecoinToModelEvent()
        self.service_defi_llama_model_stablecoin_retriever  = ServiceDefiLlamaModelStablecoinRetriever()
        self._store_db_defi_llama_stablecoin_last_updated   = StoreDefi.store_db_defi_stablecoin_llama_last_updated
        self._defi_llama_refresh_increment                  = os.environ.get('DEFI_LLAMA_STABLECOIN_REFRESH_INCREMENT', 5)

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

    @staticmethod
    def extract_price(text):
        match = re.search(r'\$(\d+\.\d+)', text)
        if match:
            return float(match.group(1))
        return None

    def send_and_save_event(self, event):
        self._service_send_model_event_to_ms_teams.send_message(
            source=EnumSource.DEFI_LLAMA_STABLECOINS.name, 
            ms_teams_message=event.ms_teams_message
        )
        event.save()

    @transaction.atomic
    @override
    def update_db(self):
        try:
            model_stablecoins = self.service_defi_llama_model_stablecoin_retriever.retrieve()
            
            now = int(datetime.now().timestamp()) * 1000
            start_timeframe = now - (int(1.15 * int(self._defi_llama_refresh_increment) * 60 * 1000))
            
            if not model_stablecoins:
                self.model_event().objects.filter(event_completed=False).update(event_completed=True)
                ts = self.model_db_last_updated()(last_updated=now)
                self.store_db_last_updated().set(ts)
                return
            
            model_event_objects = [
                self.converter_model_defi_stablecoin_to_model_event.convert(source=EnumSource.DEFI_LLAMA_STABLECOINS, model_stablecoin=x) 
                for x in model_stablecoins
            ]

            # Get depeg events from DB within timeframe and event_completed=False
            existing_events_db = self.model_event().objects.filter(event_completed=False, release_date__gte=start_timeframe)

            for event in model_event_objects:
                existing_event = existing_events_db.filter(network_tokens=event.network_tokens, alert_category=event.alert_category).first()
                
                if existing_event:
                    existing_price = self.extract_price(existing_event.title)
                    current_price = self.extract_price(event.title)
                    
                    if not existing_price:  # If no price found in existing_event title
                        continue
                    
                    price_difference_percentage = abs(current_price - existing_price) / existing_price * 100
                    
                    if price_difference_percentage >= 3:
                        existing_event.event_completed = True
                        existing_event.save()
                        self.send_and_save_event(event)

                else:
                    # This is a new event, so just save it and send a message
                    self.send_and_save_event(event)

            ts = self.model_db_last_updated()(last_updated=now)
            self.store_db_last_updated().set(ts)

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: ERROR - {e}")
            raise