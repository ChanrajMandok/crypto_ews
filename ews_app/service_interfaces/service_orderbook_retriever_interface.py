import os
import abc
import requests

from decimal import Decimal
from datetime import datetime

from ews_app.model.model_quote import ModelQuote
from ews_app.model.model_order_book import ModelOrderBook


class ServiceOrderBookRetrieverInterface(metaclass=abc.ABCMeta):
    
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
    def key_1(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def symbol_key(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def time_key(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def bid_price_key(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def bid_volume_key(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def ask_price_key(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def ask_volume_key(self):
        raise NotImplementedError

    @abc.abstractmethod
    def source(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def base_ccys(self):
        raise NotImplementedError


    def retrieve(self) -> dict[ModelQuote]:

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
                    timeout=timeout
                )

                code_group = response.status_code - (response.status_code % 100)
                if code_group != 200:
                    self.logger_instance.error(
                        f"{self.class_name} {response.status_code} - "
                        f"ERROR: Failed to get a response. "
                        f"{self.dict_url}")
                    tries += 1
                    continue

                response_raw = response.json()
                if self.key_1:
                    if not str(self.key_1) in response_raw:
                        self.logger_instance.error(
                        f"{self.class_name}: {self.url} failed to get the book tickers")
                        tries += 1
                        continue

                    orderbook_data = response_raw[self.key_1]
                else:
                    orderbook_data = response_raw

                prices_dict = {}

                for orderbook in orderbook_data:

                    symbol = orderbook[str(self.symbol_key)]
                    if not symbol:
                        self.logger_instance.error(
                        f"{self.class_name}: failed to get the orderbooks, check response formatting")
                        tries += 1
                        continue

                    if symbol not in self.tickers_list:
                        continue

                    if '-' in symbol:
                        internal_symbol = symbol.replace('-', '/')
                    else:
                        for base_ccy in self.base_ccys:
                            # Check if symbol ends with one of the base currencies
                            if symbol.endswith(base_ccy):
                                # Split the symbol into its constituents and join them with '/'
                                internal_symbol = f"{symbol[:-len(base_ccy)]}/{base_ccy}"
                                break

                    if self.time_key:
                        time = int(orderbook[self.time_key])
                    else:
                        time = int(datetime.now().timestamp()) * 1000
                        
                    if (Decimal(str(orderbook[self.bid_volume_key])) == Decimal('0')) or (Decimal(str(orderbook[self.ask_volume_key])) == Decimal('0')):
                        continue
                    
                    if (Decimal(str(orderbook[self.bid_price_key])) == Decimal('0')) or (Decimal(str(orderbook[self.ask_price_key]))== Decimal('0')):
                        continue
                        
                    bid = ModelQuote(
                                     timestamp = time,
                                     price     = Decimal(str(orderbook[self.bid_price_key])),
                                     volume    = Decimal(str(orderbook[self.bid_volume_key])),
                                     source    = self.source
                                    )
                    
                    ask = ModelQuote(
                                     timestamp = time,
                                     price     = Decimal(str(orderbook[self.ask_price_key])),
                                     volume    = Decimal(str(orderbook[self.ask_volume_key])),
                                     source    = self.source
                                    )

                    prices_dict[internal_symbol] = ModelOrderBook(symbol=internal_symbol, source_symbol=symbol, bid=bid, ask=ask, source=self.source)

                # self.logger_instance.info(
                #     f"{self.class_name}: {len(prices_dict)} {self.source.name} orderbooks retrieved..")

                return prices_dict
            
            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue