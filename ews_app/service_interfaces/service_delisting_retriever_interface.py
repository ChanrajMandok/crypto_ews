import os
import abc
import requests


class ServiceDelistingRetrieverInterface(metaclass=abc.ABCMeta):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'retreive') and
                callable(subclass.retreive))
        
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def tickers_list(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def url(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def headers(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def key_1(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def symbol_key(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def expiry_key(self):
        raise NotImplementedError

    @abc.abstractmethod
    def source(self):
        raise NotImplementedError
    
    def retrieve(self) -> dict:

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
                    url=self.url,
                    headers=self.headers,
                    timeout=timeout
                )

                code_group = response.status_code - (response.status_code % 100)
                if code_group != 200:
                    self.logger_instance.error(
                        f"{self.class_name} {response.status_code} - "
                        f"ERROR: Failed to get a response. "
                        f"{self.url}")
                    continue

                response_raw = response.json()
                if not str(self.key_1) in response_raw:
                    self.logger_instance.error(
                        f"{self.class_name}: {self.url} failed tickers infomation")
                    return {}
                ticker_data = response_raw[self.key_1]

                delisting_tickers = {}

                for t_data in ticker_data:

                    symbol = t_data[str(self.symbol_key)]
                    if not symbol:
                        self.logger_instance.error(
                            f"{self.class_name}: failed to get the delisting infomation, check response formatting")

                    if symbol not in self.tickers_list:
                        continue

                    delisting_ack = t_data[self.expiry_key]
                    if not delisting_ack:
                        continue

                    if '-' in symbol:
                        wx_symbol = symbol.replace('-', '')
                    else:
                        wx_symbol = symbol

                return delisting_tickers
            
            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue
