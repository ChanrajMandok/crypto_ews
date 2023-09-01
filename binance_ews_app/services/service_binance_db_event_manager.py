from datetime import datetime

from binance_ews_app.model.model_binance_event import \
                                        ModelBinanceEvent
from binance_ews_app.services.service_send_binance_event_to_ms_teams import \
                                        ServiceSendModelBinanceEventToMsTeams
from ews_app.enum.enum_priority import EnumPriority


class ServiceBinanceDbEventManager:

    def __init__(self) -> None:
        self.__service_send_binance_event_to_ms_teams = ServiceSendModelBinanceEventToMsTeams()

    def manage_db(self):
        now = int(datetime.now().timestamp())*1000  # Current timestamp
        incomplete_events = ModelBinanceEvent.objects.filter(event_completed=False)

        expired_events = [event for event in incomplete_events if any(int(ts) < now for ts in event.important_dates)]

        for event in expired_events:
            reminder_msg = event.ms_teams_message
            reminder_msg['title'] = 'REMINDER ' + event.ms_teams_message['title']
            reminder_msg['sections'][1] = {"activityTitle": f"Priority: {EnumPriority.REMINDER}"}

            self.__service_send_binance_event_to_ms_teams.send_message(reminder_msg)

            if all(int(ts)-26000000 < now for ts in event.important_dates):
                event.event_completed = True 
                event.save()