from datetime import datetime
from django.db import transaction
from typing_extensions import override
from singleton_decorator import singleton

from token_risk_view_app.services import logger
from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.services.service_send_model_event_to_ms_teams import \
                                     ServiceSendModelEventToMsTeams
from coinmarketcap_ews_app.model.model_token_liquidity_event import \
                                             ModelTokenLiquidityEvent
from coinmarketcap_ews_app.model.model_db_liquidity_last_updated import \
                                              ModelDbLiquidityLastUpdated
from ews_app.service_interfaces.service_db_event_updater_interface import \
                                             ServiceDbEventUpdaterInterface
from coinmarketcap_ews_app.store.store_coinmarketcap import StoreCoinMarketCap
from coinmarketcap_ews_app.converters.converter_dict_to_model_token_liquidity_event import \
                                                     ConverterDictToModelTokenLiquidityEvent
from coinmarketcap_ews_app.services.service_coinmarketcap_market_liquidity_retriever import \
                                                 ServiceCoinmarketcapMarketLiquidityRetriever


@singleton
class ServiceCoinMarketCapLiquidityEventDbEventUpdater(ServiceDbEventUpdaterInterface):

    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_send_model_event_to_ms_teams      = ServiceSendModelEventToMsTeams()
        self.convert_dict_to_model_event                = ConverterDictToModelTokenLiquidityEvent()
        self.service_cm_market_liquidity_retriever      = ServiceCoinmarketcapMarketLiquidityRetriever()
        self._store_db_liquidity_last_updated           = StoreCoinMarketCap.store_db_token_liquidty_event_last_updated

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def service_send_model_event_to_ms_teams(self):
        return self._service_send_model_event_to_ms_teams

    def store_db_last_updated(self):
        return self._store_db_liquidity_last_updated 

    def model_db_last_updated(self):
        return ModelDbLiquidityLastUpdated

    def model_event(self):
        return ModelTokenLiquidityEvent
    
    def service_raw_article_keyword_classifier(self):
        pass
    
    def service_raw_article_retriever(self):
        pass
    
    def service_article_html_retriever(self):
        pass

    @transaction.atomic
    @override
    def update_db(self):
        try:
            low_liquidity_tokens = self.service_cm_market_liquidity_retriever.retrieve()
            datetime_now = datetime.now()
            now = (int(datetime_now.timestamp()) * 1000)

            if not low_liquidity_tokens:
                ts = self.model_db_last_updated()(last_updated=now)
                self.store_db_last_updated().set(ts)
                return

            alert_category = EnumHighAlertWarningKeyWords.TOKEN_LIQUIDITY_EVENT
            model_event_objects = []

            for index, token_dict in enumerate(low_liquidity_tokens):

                token = token_dict['token']
                
                title = f"{alert_category.name.replace('_', ' ').title()}: {token}"
                
                # Check if an event with the same title and event_completed=False exists
                existing_event = self.model_event().objects.filter(
                    title=title, 
                    event_completed=False
                ).first()
                
                if existing_event:
                    if len(existing_event.important_dates) < 10:
                        # Add the current datetime_now to the old event's important_dates
                        existing_event.important_dates.append(datetime_now)
                        existing_event.save(update_fields=['important_dates'])
                    else:
                        # Set the old event's event_completed to True and create a new event
                        existing_event.event_completed = True
                        existing_event.save(update_fields=['event_completed'])
                        existing_event = None
                
                if not existing_event:
                    # Create a new event if it doesn't exist or the old one was completed
                    token_liquidity_event = \
                        self.convert_dict_to_model_event.convert(
                            url=token_dict['url'], 
                            title=title, 
                            release_date=now ,
                            increment_in_seconds=int(index)+int(1),
                            network_tokens=[token],
                            alert_category=alert_category,
                            important_dates=[now], 
                            source=EnumSource.COINMARKETCAP,
                            trading_affected=True
                        )
                    model_event_objects.append(token_liquidity_event)
                    
            # Save new events to DB and send messages
            for event in model_event_objects:
                event.save()
                self._service_send_model_event_to_ms_teams.send_message(
                    source=event.source, 
                    ms_teams_message=event.ms_teams_message
                )

            ts = self.model_db_last_updated()(last_updated=now)
            self.store_db_last_updated().set(ts)

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: ERROR - {e}")
            raise