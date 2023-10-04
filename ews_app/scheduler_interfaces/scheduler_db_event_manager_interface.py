import abc
import tzlocal

from apscheduler.schedulers.background import BackgroundScheduler


class SchedularDbEventManagerInterface(metaclass=abc.ABCMeta):
    """
    Abstract base class representing a scheduler interface responsible for 
    updating and managing a database based on certain events. 
    Implementing subclasses are required to define key methods to customize 
    the scheduler's behavior.
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
    def service_db_event_manager(self) -> str:
        """
        Abstract method expected to return a service responsible for managing
        database events.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def refresh_increment_mins(self):
        """
        Abstract method expected to return the time interval (in minutes) at which the database should be
        updated.
        """
        raise NotImplementedError
        
    @abc.abstractmethod
    def max_instances(self):
        """
        Abstract method expected to return the maximum number of instances the scheduler can spawn for
        the job.
        """
        raise NotImplementedError
    
    def __init__(self) -> None:
        self._sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone())\
                    , job_defaults = {'max_instances': int(self.max_instances)})
    
    def run(self):
        """
        Starts the scheduler and schedules a job to manage the database at 
        regular intervals as defined by 'refresh_increment_mins'.
        """
        self._sched.start()
        self._sched.add_job(self.retrieve, 'cron', minute=f"*/{self.refresh_increment_mins}"\
                             , id=f'{self.class_name}', replace_existing=True)
        self.logger_instance.info(f"Starting {self.class_name}...")

    def retrieve(self):
        """
        Attempts to manage the database using the defined management service. 
        Logs the result of the management operation.
        """
        try:
            self.service_db_event_manager().manage_db()
            self.logger_instance.info(f"{self.class_name}: DB Managment, Store Managment & Teams Messaging Completed")

        except Exception as e: 
            self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
            