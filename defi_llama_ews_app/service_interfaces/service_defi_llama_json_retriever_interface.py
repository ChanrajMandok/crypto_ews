import os
import abc
import requests

from typing_extensions import override

from defi_llama_ews_app.services.service_defi_lama_url_retriever import \
                                              ServiceDefiLamaUrlRetriever

class ServiceDefiLlamaJsonRetrieverInterface(metaclass=abc.ABCMeta):
    
    """
    Abstract base class for retrieving JSON data from the DeFi Llama service.
    Any concrete implementations should implement the abstract methods to
    specify the necessary parameters for the retrieval.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'retrieve') and
                callable(subclass.retrieve))        

    def __init__(self) -> None:
        self.service_defi_lama_static_url_retriever = ServiceDefiLamaUrlRetriever()

    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def url_headers(self):
        """Expected to return the headers required for the HTTP request."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def url_json(self):
        """Expected to return the URL endpoint for fetching the JSON data."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def intial_key(self) -> str:
        """Expected to return the initial key to access the response's primary data."""
        raise NotImplementedError 
    
    @abc.abstractmethod
    def second_key(self) -> str:
        """Expected to return the secondary key to further access the data within the primary data."""
        raise NotImplementedError 
    
    @abc.abstractmethod
    def filter_results(self) -> str:
        """Expected to return filtered results from the fetched data."""
        raise NotImplementedError 

    @override
    def retrieve(self, test: bool = False):
        """Retrieves and filters JSON data from the DeFi Llama service """
        
        tries = 0
        max_tries = 3
        timeout = int(os.environ.get('TIMEOUT', 10))
        session = requests.Session()

        while tries < max_tries:
            try:
                url = self.service_defi_lama_static_url_retriever.retrieve(self.url_json)
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
                filtered_results = self.filter_results(object_list=info_dict, test=test)
                final_result = filtered_results if filtered_results else []
                return final_result 

            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue