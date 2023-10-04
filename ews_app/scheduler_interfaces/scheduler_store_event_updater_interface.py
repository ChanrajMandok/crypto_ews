import abc
import tzlocal

from apscheduler.schedulers.background import BackgroundScheduler


class SchedularStoreEventUpdaterInterface(metaclass=abc.ABCMeta):
    """
    Abstract base class representing a scheduler responsible for updating a store 
    based on certain events. Implementing subclasses are required to define key 
    methods to customize the scheduler's behavior.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'run') and
                callable(subclass.run))
        
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def service_store_event_updater(self) -> str:
        """
        Abstract method that should return a service or utility responsible 
        for updating the store based on events.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def refresh_increment_mins(self):
        """
        Abstract method expected to return the time interval (in minutes) at which the database should
        be updated.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def max_instances(self):
        """
        Abstract method expected to return the maximum number of instances the scheduler can spawn
        for the job.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def observer(self):
        """
        Abstract method that should return an observer object or mechanism 
        to monitor changes or events.
        """
        raise NotImplementedError
    
    def __init__(self) -> None:
        self._sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone())\
                    , job_defaults = {'max_instances': int(self.max_instances)})
    
    def run(self):
        """
        Starts the scheduler and adds a job to update the store at regular 
        intervals as defined by 'refresh_increment_mins'.
        """
        
        self._sched.start()
        self._sched.add_job(self.retrieve, 'cron', minute=f"*/{self.refresh_increment_mins}"\
                             , id=f'{self.class_name}', replace_existing=True)
        self.logger_instance.info(f"Starting {self.class_name}...")

    def retrieve(self):
        """
        Attempts to update the store using the defined updater service. 
        Logs the result of the update operation.
        """
        
        try:
            self.service_store_event_updater().update_store()
            self.logger_instance.info(f"{self.class_name}: Store Managment & Teams Messaging Completed")

        except Exception as e: 
            self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")