import abc

from typing import Union
from decimal import Decimal
from datetime import datetime

from ews_app.enum.enum_priority import EnumPriority
from ews_app.model.model_stablecoin import ModelStableCoin
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from defi_llama_ews_app.model.model_defi_stablecoin import ModelDefiStablecoin


class ConverterDictToModelStablecoinInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def model_stablecoin(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractproperty
    def price_key(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def mechanism_key(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def stablecoin_key(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def one_day_price_change_key(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def peg_deviation_key(self) -> str:
        raise NotImplementedError

    def convert(self, 
                url              : str,
                dict             : dict,
                trading_affected : bool,
                alert_priority   : EnumPriority,
                alert_category   : Union[EnumLowAlertWarningKeyWords, 
                                        EnumHighAlertWarningKeyWords])-> ModelDefiStablecoin:
        
        try:
            name = dict.get(self.stablecoin_key)
            model_stablecoin = ModelStableCoin.objects.get(currency=name)
        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")

        try:
            now = int(datetime.now().timestamp()) * 1000
            
            model_stablecoin = \
                self.model_stablecoin()(
                                        url                  = url, 
                                        release_date         = now,
                                        alert_category       = alert_category,
                                        alert_priority       = alert_priority,
                                        trading_affected     = trading_affected,
                                        stablecoin           = model_stablecoin,
                                        price                = Decimal(str(dict.get(self.price_key))),
                                        mechanism            = str(dict.get(self.mechanism_key)),
                                        peg_deviation        = Decimal(str(dict.get(self.peg_deviation_key))),
                                        one_day_price_change = Decimal(str(dict.get(self.one_day_price_change_key))),
                                        )
                
            return model_stablecoin

        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")