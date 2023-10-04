import abc

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_blockchain import EnumBlockchain
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency


class ConverterDictToModelBridgeHackInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def model_hack(self):
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
    def hack_amount_key(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def release_date_key(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def url_key(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def protocol_key(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def exploit_key(self) -> str:
        raise NotImplementedError
    
    @abc.abstractproperty
    def blockchain_key(self) -> str:
        raise NotImplementedError
    
    def convert(self, defi_llama_dict: dict) -> model_hack:

        try:
            alert_priority = EnumPriority.LOW.name
            alert_category = EnumHighAlertWarningKeyWords.BRIDGE_HACK

            hack_amount    = defi_llama_dict.get(self.hack_amount_key)
            release_date   = defi_llama_dict.get(self.release_date_key)
            url            = defi_llama_dict.get(self.url_key)
            protocol       = defi_llama_dict.get(self.protocol_key)
            exploit        = defi_llama_dict.get(self.exploit_key)
            blockchains    = defi_llama_dict.get(self.blockchain_key)

            trading_affected = False
            network_tokens = []
            if blockchains:
                for blockchain in blockchains:
                    try:
                        e = EnumBlockchain[blockchain.upper()].value
                    except KeyError:
                        e = None
                    if e:
                        network_tokens.append(e)  
                        if ModelWirexSpotCurrency.objects.filter(currency=e.upper()).exists():
                            alert_priority   = EnumPriority.HIGH.name
                            trading_affected = True 

            raw_hack_object = \
                self.model_hack()(
                    url              = url,
                    blockchain       = blockchains,
                    protocol         = protocol,
                    hacked_amount_m  = hack_amount,
                    release_date     = release_date,
                    exploit          = exploit,
                    alert_category   = alert_category,
                    alert_priority   = alert_priority,
                    network_tokens   = network_tokens, 
                    trading_affected = trading_affected
                )
            
            return raw_hack_object
            
        except Exception as e:
            # Logging the exception details, including the class name for clarity.
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")