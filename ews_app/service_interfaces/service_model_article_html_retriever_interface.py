import os
import abc
import time
import requests

from time import sleep
from random import randint
from datetime import datetime

from ews_app.model_interfaces.model_event_interface import \
                                         ModelEventInterface
from ews_app.model_interfaces.model_article_interface import \
                                         ModelArticleInterface
from ews_app.services.service_model_article_url_creator import \
                                    ServiceModelArticleUrlCreator


class ServiceModelArticleHtmlRetrieverInterface(metaclass=abc.ABCMeta):
    
    """
    Service iterates over the articles which have been found to have important 
    keywords & are within date range and retrieves the html of the article. 
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'retrieve') and
                callable(subclass.retrieve))

    @abc.abstractmethod
    def class_name(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def article_handler(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def base_url(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def url_headers(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def source(self):
        raise NotImplementedError

    def __init__(self) -> None:
        self._service_model_article_url_creator   = ServiceModelArticleUrlCreator()

    def retrieve(self,
                 articles: list[ModelArticleInterface],
                 test : bool = False) -> list[ModelEventInterface]:

        today = int(datetime.now().timestamp())*1000
        timeout = int(os.environ.get('TIMEOUT', 10))
        ssl_verify = False if os.environ.get('SSL_VERIFY', 'True') == "False" else True
        
        session = requests.Session()
        session.verify = ssl_verify
        
        model_event_list = []
        
        for article_object in articles:
            sleep(randint(1,3))  # Random sleep between 1 and 3 seconds

            raw_article = article_object.raw_article
            url = self._service_model_article_url_creator.create_url(
                                                                    base_url=self.base_url,
                                                                    source=self.source(),
                                                                    instance=raw_article)
    
            try:
                response = session.get(
                    url=url,
                    headers=self.url_headers,
                    timeout=timeout)

                if response.status_code == 429:
                    self.logger_instance.info(f"{self.class_name} {response.status_code} - INFO: " +
                                f"60 second break and switch to backup URL due to rate limit for: {url}.")
                    backup_url = self._service_model_article_url_creator.create_backup_url(
                                                                                   base_url=self.base_url,
                                                                                   source=self.source,
                                                                                   instance=raw_article)
                    if backup_url:
                        time.sleep(60)
                        response = session.get(
                            url=backup_url,
                            headers=self.url_headers,
                            timeout=timeout
                        )

            except requests.RequestException as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue

            if response.status_code - (response.status_code % 100) != 200:
                self.logger_instance.error(f"{self.class_name} {response.status_code} - ERROR: " +
                            f"Failed to get a response from URL: {url}")
                continue
            
            decoded_content = response.content.decode('utf-8')

            if not decoded_content.lstrip().startswith(('<!DOCTYPE', '<html')) or \
                '<body' not in decoded_content:
                self.logger_instance.error(f"{self.class_name} - ERROR: Invalid HTML received for URL: {url}.")
                continue
            
            article_object.url = url
            article_object.html = response.content
            
            model_event = self.article_handler().handle(article_object)
            if test:
                model_event_list.append(model_event)
            else:
                if max(model_event.important_dates) > today:
                    model_event.important_dates = [x for x in model_event.important_dates if x > today]
                    model_event_list.append(model_event)           
            
        return model_event_list

        