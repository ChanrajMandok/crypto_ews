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

