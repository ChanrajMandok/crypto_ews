import abc
import tzlocal

from apscheduler.schedulers.background import BackgroundScheduler


class SchedularStoreEventUpdaterInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'run') and
                callable(subclass.run))
        
    @abc.abstractmethod
    def class_name(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def service_store_event_updater(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def refresh_increment_mins(self):
        raise NotImplementedError
        
    @abc.abstractmethod
    def max_instances(self):
        raise NotImplementedError
    
    def __init__(self) -> None:
        self._sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone())\
                    , job_defaults = {'max_instances': int(self.max_instances)})
    
    def run(self):
        self._sched.start()
        self._sched.add_job(self.retrieve, 'cron', minute=f"*/{self.refresh_increment_mins}"\
                             , id=f'{self.class_name}', replace_existing=True)
        self.logger_instance.info(f"Starting {self.class_name}...")

    def retrieve(self):

        try:
            self.service_store_event_updater().update_store()
            self.logger_instance.info(f"{self.class_name}: Store Managment & Teams Messaging Completed")

        except Exception as e: 
            self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")