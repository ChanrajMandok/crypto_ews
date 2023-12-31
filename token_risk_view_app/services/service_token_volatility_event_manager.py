from datetime import datetime
from django.db import transaction
from singleton_decorator import singleton

from ews_app.enum.enum_source import EnumSource
from token_risk_view_app.services import logger
from ews_app.services.service_send_model_event_to_ms_teams import \
                                     ServiceSendModelEventToMsTeams
from token_risk_view_app.model.model_token_volatility_event import \
                                           ModelTokenVolatilityEvent


@singleton
class ServiceTokenVolatilityEventManager():

    def __init__(self) -> None:
        self.logger_instance = logger
        self._is_locked = False
        self.class_name = self.__class__.__name__
        self.service_send_model_event_to_ms_teams = ServiceSendModelEventToMsTeams()

    @transaction.atomic
    def manage_db(self, pretty_increment: str, token_volatility_event: ModelTokenVolatilityEvent):
        """
        Manages the database for token volatility events.

        For a given token_volatility_event, the function updates any intersecting tickers from the event 
        and marks the event as completed if all of its important dates have passed.
        """
        
        # Avoid multiple concurrent executions
        if self._is_locked:
            self.logger_instance.warning("manage_db is already running. Exiting this run.")
            return
        self._is_locked = True
        
        try:    
            affected_tokens = set(token_volatility_event.h_spot_tickers)                
            now = int(datetime.now().timestamp()) * 1000

            # Fetch all open events
            open_token_volatility_events = ModelTokenVolatilityEvent.objects.filter(
                                                event_completed=False
                                            ).order_by('release_date')

            expired_event_ids = []  # To store IDs of events that are expired
            for open_token_volatility_event in open_token_volatility_events:

                # Check and update tickers
                if open_token_volatility_event.title.__contains__(pretty_increment):
                    common_tickers =\
                          affected_tokens.intersection(set(open_token_volatility_event.h_spot_tickers))
                    if common_tickers:
                        open_token_volatility_event.h_spot_tickers = [ticker for ticker in \
                            open_token_volatility_event.h_spot_tickers if ticker not in common_tickers]
                        open_token_volatility_event.l_spot_tickers = [ticker for ticker in common_tickers]
                        open_token_volatility_event.save()

                # Check if the event is expired
                if all(int(date) < now for date in open_token_volatility_event.important_dates) or \
                                                            not open_token_volatility_event.h_spot_tickers:
                    expired_event_ids.append(open_token_volatility_event.id)

            # Directly update expired events outside of the loop
            ModelTokenVolatilityEvent.objects.filter(id__in=expired_event_ids).update(event_completed=True)

            self.service_send_model_event_to_ms_teams.send_message(source=EnumSource.BINANCE_ORDERBOOKS.name, 
                                                                   ms_teams_message=token_volatility_event.ms_teams_message)

            token_volatility_event.save()

        except Exception as e:
                self.logger_instance.error(f"{self.class_name}: manage_db ERROR: {str(e)}")
        finally:
            # Release the lock
            self._is_locked = False