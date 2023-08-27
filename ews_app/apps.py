import sys

from ews_app import logger
from django.apps import AppConfig


class EwsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ews_app'

    def ready(self):
        
        if ('markets.wsgi:application' in sys.argv) or ('runserver' in sys.argv):
            
            logger.info("EwsAppConfig: getting ready")

        from binance_ews_app.observers.observer_binance_store_event_updater import \
                                                        ObserverBinanceStoreEvent
        ObserverBinanceStoreEvent()
        
        from binance_ews_app.scheduler.scheduler_binance_event_store_updater import \
                                                    SchedularBinanceEventStoreUpdater

        SchedularBinanceEventStoreUpdater().run()
        
