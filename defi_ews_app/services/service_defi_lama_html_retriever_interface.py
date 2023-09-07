import os
import abc
import brotli
import requests

from bs4 import BeautifulSoup


class ServiceDefiLamaHtmlRetrieverInterface(metaclass=abc.ABCMeta):

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
    def url_headers(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def url(self):
        raise NotImplementedError

    @abc.abstractmethod
    def table_selector(self):
        raise NotImplementedError

    def retrieve(self):

        tries = 0
        max_tries = 3
        timeout = int(os.environ.get('TIMEOUT', 10))
        session = requests.Session()
        url = self.url

        while tries < max_tries:
            try:
                response = session.get(
                    url=url,
                    headers=self.url_headers,
                    timeout=timeout)
                
                if response.status_code - (response.status_code % 100) != 200:
                    self.logger_instance.error(f"{self.class_name} {response.status_code}\
                                               - ERROR: " +f"Failed to get a response from URL: {url}")
                    tries += 1
                    continue

                content_type = response.headers.get('Content-Type')
                if 'text/html' not in content_type:
                    self.logger_instance.error(f"{self.class_name} - ERROR: " +
                            f"Content in the wrong format from URL: {url}")
                    tries += 1
                    continue

                # brotli package required to parse 'br' content encoding with no additional code
                html_content = response.content

                soup = BeautifulSoup(html_content, 'html.parser')
                table_body = soup.select_one(self.table_selector)

                if not table_body:
                    self.logger_instance.error(f"{self.class_name} - ERROR: check css selector logic")
                    continue                
                else:
                    return table_body

            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue