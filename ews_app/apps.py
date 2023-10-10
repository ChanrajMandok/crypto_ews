import sys


from ews_app import logger
from django.apps import AppConfig



class EwsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ews_app'

    def ready(self):

        blocked_commands = ['migrate', 'makemigrations', 'script_populate_tables', 'flush', 'shell_plus', 'test']

        if not any(command in sys.argv for command in blocked_commands):
            logger.info(f"{self.__class__.__name__}:  Getting Ready")

            from binance_ews_app.scheduler.scheduler_binance_event_db_updater import \
                SchedularBinanceEventDbUpdater

            SchedularBinanceEventDbUpdater().run()

            from binance_ews_app.scheduler.scheduler_binance_event_db_manager import \
                SchedularBinanceEventDbManager

            SchedularBinanceEventDbManager().run()

            from okx_ews_app.scheduler.scheduler_okx_event_db_updater import \
                SchedularOkxEventDbUpdater

            SchedularOkxEventDbUpdater().run()

            from okx_ews_app.scheduler.scheduler_okx_event_db_manager import \
                SchedularOkxEventDbManager

            SchedularOkxEventDbManager().run()
            
            from defi_llama_ews_app.scheduler.scheduler_defi_llama_hack_event_db_updater import \
                SchedularDefiLlamaHackEventDbUpdater
                
            SchedularDefiLlamaHackEventDbUpdater().run()

            from defi_llama_ews_app.scheduler.scheduler_defi_llama_stablecoin_event_db_updater import \
                SchedularDefiLlamaStableCoinEventDbUpdater
            
            SchedularDefiLlamaStableCoinEventDbUpdater().run()

            from defi_llama_ews_app.scheduler.scheduler_defi_lama_bridge_hack_event_db_updater import \
                SchedularDefiLlamaBridgeHackEventDbUpdater

            SchedularDefiLlamaBridgeHackEventDbUpdater().run()

            from token_risk_view_app.scheduler.scheduler_token_price_change_store_updater import \
                                                            SchedulerTokenPriceChangeStoreUpdater
            
            SchedulerTokenPriceChangeStoreUpdater().run()