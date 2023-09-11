import abc 

from dateutil import parser

from ews_app.enum.enum_priority import EnumPriority
from ews_app.model.model_wirex_spot_currency import \
                                ModelWirexSpotCurrency
from ews_app.enum.enum_high_alert_warning_key_words \
                    import EnumHighAlertWarningKeyWords
from ews_app.enum.enum_blockchain import EnumBlockchain


class ConverterListToModelHackRawInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))
    
    @abc.abstractmethod
    def model_hack(self):
        raise NotImplementedError   
    
    @abc.abstractmethod
    def class_name(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        raise NotImplementedError
    
    @abc.abstractproperty
    def protocol_list_index(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def url_list_index(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def release_date_list_index(self) -> str:
        raise NotImplementedError
        
    @abc.abstractproperty
    def hacked_amount_list_index(self) -> str:
        raise NotImplementedError
    
    @abc.abstractproperty
    def blockchain_list_index(self) -> str:
        raise NotImplementedError
    
    @abc.abstractproperty
    def exploit_list_index(self) -> str:
        raise NotImplementedError
    
    @staticmethod
    def get_or_none(value: str) -> str:
        return value if value and value.strip() != '' else None

    def convert(self, defi_lama_dict: dict) -> model_hack:

        try:
            alert_priority = EnumPriority.LOW.name
            alert_category = EnumHighAlertWarningKeyWords.HACK.name

            hack_string       = self.get_or_none(defi_lama_dict[int(self.hacked_amount_list_index)])
            blockchain_string = self.get_or_none(defi_lama_dict[int(self.blockchain_list_index)])
            protocol          = self.get_or_none(defi_lama_dict[int(self.protocol_list_index)].replace(' ','_'))
            url_str           = self.get_or_none(defi_lama_dict[int(self.url_list_index)])
            
            datetime_str = self.get_or_none(defi_lama_dict[int(self.release_date_list_index)])
            datetime = parser.parse(datetime_str) if datetime_str else None

            blockchains = [self.get_or_none(chain.split('/')[-1]) for chain in blockchain_string.split(';')] if blockchain_string else []
            if blockchains and blockchains[0] and blockchains[0].startswith('+'):
                blockchains.pop(0)

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
                    
            hack_amount = float(hack_string.replace('$', '').replace('m', '')) if hack_string else None

            raw_hack_object = \
                self.model_hack()(
                    url              = url_str,
                    blockchain       = blockchains,
                    protocol         = protocol,
                    hacked_amount_m  = hack_amount,
                    release_date     = int(datetime.timestamp() * 1000) if datetime else None,
                    exploit          = self.get_or_none(defi_lama_dict[int(self.exploit_list_index)]),
                    alert_category   = alert_category,
                    alert_priority   = alert_priority,
                    network_tokens   = network_tokens, 
                    trading_affected = trading_affected
                )
            
            return raw_hack_object
            
        except Exception as e:
            # Logging the exception details, including the class name for clarity.
            self.logger_instance.error(f"{self.class_name} - ERROR: {e}")