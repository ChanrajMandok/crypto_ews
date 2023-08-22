import os
import tzlocal
import asyncio

from singleton_decorator import singleton
from apscheduler.schedulers.background import BackgroundScheduler


from binance_ews_app.scheduler import logger

class SchedularBinanceAlertsRefresh:
    
    def __init__(self) -> None:
        self.__sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
        
        
    
    def run(self):

        logger.info(f"{__class__.__name__}: Starting scheduler...")
        self.__sched.start()
        pass