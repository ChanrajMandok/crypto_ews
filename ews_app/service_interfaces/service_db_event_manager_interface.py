import abc

from datetime import datetime

from ews_app.enum.enum_priority import EnumPriority
from ews_app.services.service_send_model_event_to_ms_teams import \
                                     ServiceSendModelEventToMsTeams


class ServiceDbEventManagerInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'manage_db') and
                callable(subclass.manage_db))
        
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def model_event(self):
        raise NotImplementedError

    def __init__(self) -> None:
        self._service_send_binance_event_to_ms_teams = ServiceSendModelEventToMsTeams()

    def manage_db(self):
        now = int(datetime.now().timestamp()) * 1000  # Current timestamp
        incomplete_events = self.model_event().objects.filter(event_completed=False)

        for event in incomplete_events:
            source = event.source 
            event_priority = event.alert_priority
            expired_dates = [int(ts) for ts in event.important_dates if int(ts) < now]

            if expired_dates and event_priority == EnumPriority.HIGH.value:
                # Send message to MS Teams for the expired dates
                reminder_msg = event.ms_teams_message
                reminder_msg['title'] = 'REMINDER ' + event.ms_teams_message['title']
                reminder_msg['sections'][1] = {"activityTitle": f"Priority: {EnumPriority.REMINDER.name}"}
                self._service_send_binance_event_to_ms_teams.send_message(source=source, 
                                                                          ms_teams_message=reminder_msg)
        
            if expired_dates:
                # Pop the expired dates from the event's important_dates list
                event.important_dates = [ts for ts in event.important_dates if int(ts) > now]
                
                # If the important_dates list is empty, set the event as completed
                if not event.important_dates:
                    event.event_completed = True
                event.save()

                # Check if all dates are expired, mark the event as completed
                if all(int(ts) - 26000000 < now for ts in event.important_dates):
                    event.event_completed = True
                    event.save()
