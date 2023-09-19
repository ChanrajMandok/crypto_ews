import os
import abc
import time
import requests


class ServiceRawArticleRetrieverInterface(metaclass=abc.ABCMeta):
    """
    Services finds the latest articles headlines released from Binance announcements Page 
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
    def base_url(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def dict_url(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def url_headers(self):
        raise NotImplementedError

    @abc.abstractproperty
    def nested_key_1(self) -> str:
        raise NotImplementedError

    def retrieve(self):

        tries = 0
        max_tries = 3
        ssl_env = os.environ.get('SSL_VERIFY', 'True')
        ssl_verify = False if ssl_env == "False" else True
        timeout = int(os.environ.get('TIMEOUT', 1000))

        while tries < max_tries:
            try:
                session = requests.Session()
                session.verify = ssl_verify
                response = session.get(
                    url=self.dict_url,
                    headers=self.url_headers,
                    timeout=timeout
                )

                if response.status_code == 429 and not response.content:
                    self.logger_instance.warning(
                        f"{self.class_name} {response.status_code} - "
                        f"Received a rate limit warning. "
                        f"Sleeping for 60 seconds...")
                    time.sleep(60)
                    tries += 1
                    continue

                code_group = response.status_code - (response.status_code % 100)
                if code_group != 200:
                    self.logger_instance.error(
                        f"{self.class_name} {response.status_code} - "
                        f"ERROR: Failed to get a response. "
                        f"{self.dict_url}")
                    tries += 1
                    continue

                response_json = response.json()
                data = response_json.get('data')
                if not data:
                    msg = (f"{self.class_name} - ERROR: 'data' attribute "
                           f"missing in the {self.dict_url} response.")
                    self.logger_instance.error(msg)
                    tries += 1
                    continue

                catalogues = data.get(self.nested_key_1)
                if not catalogues:
                    msg = (f"{self.class_name} - ERROR: 'catalogs' "
                           f"attribute missing in {self.dict_url} response.")
                    self.logger_instance.error(msg)
                    tries += 1
                    continue

                return catalogues

            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue

        return []