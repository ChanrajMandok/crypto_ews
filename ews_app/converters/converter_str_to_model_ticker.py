from binance_ews_app.converters import logger
from ews_app.model.model_ticker import ModelTicker
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_currency_type import EnumCurrencyType
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency
from ews_app.model.model_wirex_usdm_currency import ModelWirexUsdmCurrency


class ConverterStrToModelTicker:

    def convert(self, ticker_str: str, type: EnumCurrencyType) -> ModelTicker:
        
        """
        Convert a string in the format 'XXXX/XXXX' to a ModelTicker instance.

        Parameters:
        - ticker_str: The ticker string to convert.
        - type: The type of currency (SPOT or USDM).

        Returns:
        - A new ModelTicker instance or None in case of an error.
        """
        
        try:
            base, quote = ticker_str.split('/')
            
            # Initialize as LOW. If currency exists in db table, it will be set to HIGH.
            priority = EnumPriority.LOW.name
            
            if type == EnumCurrencyType.SPOT:
                if ModelWirexSpotCurrency.objects.filter(currency=base).exists() and \
                quote in ['BTC', 'USDT']:
                    priority = EnumPriority.HIGH.name
                    
            elif type == EnumCurrencyType.USDM:
                if ModelWirexUsdmCurrency.objects.filter(currency=base).exists():
                    priority = EnumPriority.HIGH.name

            ticker = ModelTicker(
                name           = ticker_str,
                base_currency  = base,
                quote_currency = quote,
                alert_priority = priority,
                currency_type  = type.value
            )
            
            return ticker
        
        except ValueError:
            logger.error(f"{self.__class__.__name__} - ERROR: Invalid ticker format.z\
                                        Expected format 'BASE/QUOTE', got {ticker_str}.")
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - ERROR: {e}")

        return None
