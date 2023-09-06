from datetime import datetime

from ews_app.enum.enum_priority import EnumPriority
from binance_ews_app.model.model_binance_event import \
                                        ModelBinanceEvent
from ews_app.services.service_send_binance_event_to_ms_teams \
                           import ServiceSendModelBinanceEventToMsTeams


class ServiceBinanceDbEventManager:

    def __init__(self) -> None:
        self.__service_send_binance_event_to_ms_teams = ServiceSendModelBinanceEventToMsTeams()

    def manage_db(self):
        now = int(datetime.now().timestamp()) * 1000  # Current timestamp
        incomplete_events = ModelBinanceEvent.objects.filter(event_completed=False)

        for event in incomplete_events:
            expired_dates = [int(ts) for ts in event.important_dates if int(ts) < now]

            if expired_dates:
                # Send message to MS Teams for the expired dates
                reminder_msg = event.ms_teams_message
                reminder_msg['title'] = 'REMINDER ' + event.ms_teams_message['title']
                reminder_msg['sections'][1] = {"activityTitle": f"Priority: {EnumPriority.REMINDER.name}"}
                self.__service_send_binance_event_to_ms_teams.send_message(reminder_msg)

                # Pop the expired dates from the event's important_dates list
                event.important_dates = [ts for ts in event.important_dates if int(ts) not in expired_dates]
                
                # If the important_dates list is empty, set the event as completed
                if not event.important_dates:
                    event.event_completed = True
                event.save()

                # Check if all dates are expired, mark the event as completed
                if all(int(ts) - 26000000 < now for ts in event.important_dates):
                    event.event_completed = True
                    event.save()
