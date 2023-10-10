import time

from datetime import datetime
from singleton_decorator import singleton

from django.db import transaction
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
        self._service_send_model_event_to_ms_teams = ServiceSendModelEventToMsTeams()

    @transaction.atomic  # Ensure atomic transactions
    def manage_db(self, pretty_increment: str, token_volatility_event:ModelTokenVolatilityEvent):
        
        # Avoid multiple concurrent executions
        if self._is_locked:
            self.logger_instance.warning("manage_db is already running. Exiting this run.")
            return
        self._is_locked = True
        
        try:    
            affected_tokens = set(token_volatility_event.h_spot_tickers)
                    
            now = int(datetime.now().timestamp()) * 1000

            open_token_volatility_events = ModelTokenVolatilityEvent.objects.filter(
                                                title__icontains=pretty_increment,
                                                event_completed=False
                                              ).order_by('release_date')

            for open_token_volatility_event in open_token_volatility_events:
                
                common_tickers = affected_tokens.intersection(set(open_token_volatility_event.h_spot_tickers))
                
                if common_tickers:
                    open_token_volatility_event.h_spot_tickers = [ticker for ticker in open_token_volatility_event.h_spot_tickers if ticker not in common_tickers]
                    open_token_volatility_event.save()

                if all(int(date) < now for date in open_token_volatility_event.important_dates) or not open_token_volatility_event.h_spot_tickers:
                    open_token_volatility_event.event_completed = True
                    open_token_volatility_event.save()

            token_volatility_event.save()

        except Exception as e:
            # For handling back-off strategy (you can refine this further)
            for _ in range(3):  # Try 3 time
                time.sleep(5)  
                self.logger_instance.warning("Retrying due to error: {}".format(e))
                self.manage_db(pretty_increment, token_volatility_event)
            else:
                self.logger_instance.error(f"{self.class_name}: manage_db ERROR: {str(e)}")
        finally:
            # Release the lock
            self._is_locked = False