import os
import tzlocal

from singleton_decorator import singleton
from apscheduler.schedulers.background import BackgroundScheduler

from binance_ews_app.scheduler import logger
from binance_ews_app.services.service_binance_store_event_updater import \
                                                    ServiceStoreEventUpdater


@singleton
class SchedularBinanceEventStoreUpdater:
    
    def __init__(self) -> None:
        self.__refresh_increment_mins = int(os.environ.get('REFRESH_INCREMENT_MINS', 5))
        self.__service_binance_store_event_updater = ServiceStoreEventUpdater()
        self.__sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone())\
                    , job_defaults = {'max_instances': 1})
    
    def run(self):
        logger.info(f"{__class__.__name__}: Starting scheduler...")
        self.__sched.start()
        self.__sched.add_job(self.retrieve, 'cron', minute=f"*/{self.__refresh_increment_mins}"\
                             , id=f'{self.__class__.__name__}', replace_existing=True)

    def retrieve(self):

        try:
            self.__service_binance_store_event_updater.update_store()
            logger.info(f"{__class__.__name__}: Store being updated")

        except Exception as e: 
            logger.error(f"{self.__class__.__name__} - ERROR: {str(e)}")
            