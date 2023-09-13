import os
import abc
import requests


class ServiceDefiLlamaJsonRetrieverInterface(metaclass=abc.ABCMeta):

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
    def intial_key(self) -> str:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def second_key(self) -> str:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def filter_results(self) -> str:
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

                response_json = response.json()
                data = response_json.get(str(self.intial_key))

                if not data:
                    msg = f"{self.class_name} - ERROR: 'data' attribute missing in the {self.intial_key} response."
                    self.logger_instance.error(msg)
                    tries += 1
                else:
                    info_dict = data.get(str(self.second_key))
                    if not info_dict:
                        msg = f"{self.class_name} - ERROR: 'data' attribute missing in the {self.second_key} response."
                        self.logger_instance.error(msg)
                        tries += 1

                ## this will only be populated if there are stablecoins which are depegged (<0.05)
                filtered_results = self.filter_results(stablecoins=info_dict)
                final_result = filtered_results if filtered_results else []
                return final_result 

            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue