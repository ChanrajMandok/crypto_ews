import abc

from datetime import datetime
from django.db import transaction


class ServiceDbEventUpdaterInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'update_db') and
                callable(subclass.update_db))
        
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def service_raw_article_retriever(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def service_article_html_retriever(self):
        raise NotImplementedError

    @abc.abstractmethod
    def service_send_model_event_to_ms_teams(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def store_db_last_updated(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def service_raw_article_keyword_classifier(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def model_db_last_updated(self):
        raise NotImplementedError

    @abc.abstractmethod
    def model_event(self):
        raise NotImplementedError

    @transaction.atomic
    def update_db(self):
        try:
            # Retrieve all recent news articles & announcements from binance
            articles = self.service_raw_article_retriever().retrieve()
            
            # Filter news articles & announcements for specific values
            key_articles = self.service_raw_article_keyword_classifier().classify_articles(raw_articles=articles)
            
            # Now pull HTML of articles from binance
            model_event_objects = self.service_article_html_retriever().retrieve(key_articles)

            now = int(datetime.now().timestamp()) * 1000
            # If there are no model event objects, exit early.
            if not model_event_objects:
                ts = self.model_db_last_updated()(last_updated=now)
                self.store_db_last_updated().set(ts)
                return

            # Check for duplicates and filter them out using the 'id' field
            existing_ids = self.model_event().objects.filter(id__in=[x.id for x in model_event_objects]).values_list('id', flat=True)
            
            new_events = [event for event in model_event_objects if event.id not in existing_ids]
            
            # Save to DB and send messages for new events
            for event in new_events:
                source = event.source
                self.service_send_model_event_to_ms_teams().send_message(source=source, 
                                                                        ms_teams_message=event.ms_teams_message)
                event.save()

            ts = self.model_db_last_updated()(last_updated=now)
            self.store_db_last_updated().set(ts)

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: ERROR - {e}")
            raise
            
            