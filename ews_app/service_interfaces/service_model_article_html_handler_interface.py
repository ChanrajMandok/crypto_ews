import re
import abc

from typing import Union
from dateutil import parser

from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.enum.enum_currency_type import EnumCurrencyType
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.model_interfaces.model_article_interface import \
                                         ModelArticleInterface
from ews_app.converters.converter_str_to_model_ticker import \
                                     ConverterStrToModelTicker
from ews_app.model.model_spot_currency import ModelSpotCurrency
from ews_app.services.service_extract_article_content_from_html import \
                                    ServiceExtractArticleContentFromHtml
from ews_app.model_interfaces.model_event_interface import ModelEventInterface


class ServiceModelArticleHtmlHandlerInterface(metaclass=abc.ABCMeta):
    """
    Service extracts important Dates, articles, trading pairs, 
    and specific contract trading pairs from HTML format.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """ Helper to determine if a class provides the 'retrieve' method. """
        
        return (hasattr(subclass, 'handle') and
                callable(subclass.handle))
    
    @abc.abstractmethod
    def class_name(self) -> str:
        """Expected to return the name of the class."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def logger_instance(self):
        """Expected to return a logger instance for logging purposes."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_pairs(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_date(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_network_upgrade(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_contract_swap(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_contract_pairs(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_base_quote(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def pattern_trading_not_affected(self):
        raise NotImplementedError

    @abc.abstractmethod
    def pattern_trading_affected(self):
        raise NotImplementedError

    @abc.abstractmethod
    def converter_a_to_e(self):
        raise NotImplementedError 
    
    @abc.abstractmethod
    def source(self):
        raise NotImplementedError
    
    def __init__(self):
        self._converter_str_to_model_ticker           = ConverterStrToModelTicker()
        self._service_extract_article_from_html       = ServiceExtractArticleContentFromHtml()

    def handle(self, article: ModelArticleInterface) -> ModelEventInterface:

        try:
            source               = self.source()
            release_date_ts      = article.raw_article.release_date
            category             = article.alert_category
            article_content_text = \
                self._service_extract_article_from_html.extract_article_content(source=source,
                                                                                article_html_content=article.html)

            h_spot_tickers, l_spot_tickers = self.extract_spot_pairs(article_content_text)

            ## only look for USDM pairs in Binance Articles
            if source == EnumSource.BINANCE:
                h_usdm_tickers, l_usdm_tickers = self.extract_usdm_pairs(article_content_text)
            else:
                h_usdm_tickers, l_usdm_tickers = [], [] 
            
            important_dates = self.extract_important_dates(content=article_content_text,
                                                           release_date=release_date_ts)
            trading_affected = self.extract_trading_status(content=article_content_text,
                                                            alert_category=category)
            network_tokens = self.extract_network_token(content=article_content_text,
                                                            alert_category=category)
            internal_ccy_affected = any(ModelSpotCurrency.objects.filter(currency=x).exists() \
                                                                            for x in network_tokens)
            
            if (h_spot_tickers or h_usdm_tickers) or \
                (category.value in ['hard', 'fork', 'upgrade', 'contract'] \
                                    and trading_affected and internal_ccy_affected):
                article.alert_priority = EnumPriority.HIGH.name
            
            event = self.converter_a_to_e().convert(
                source=source,
                article=article,
                network_tokens=network_tokens,
                h_spot_tickers=h_spot_tickers,
                h_usdm_tickers=h_usdm_tickers,
                l_spot_tickers=l_spot_tickers,
                l_usdm_tickers=l_usdm_tickers,
                important_dates=important_dates,
                trading_affected=trading_affected,
            )
            return event
            
        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - Unexpected error: {str(e)}\
                                        for article: {article.raw_article.title}")

    def extract_important_dates(self, content: str, release_date: int) -> list[int]:
        if not isinstance(release_date, int) or release_date <= 0:
            self.logger_instance.error(f"{self.class_name} - Invalid release_date value: {release_date}")
            return []

        important_date_strings = [match for match in self.pattern_date.findall(content)]
            
        # Initialize the set with the release_date
        important_dates = {release_date}
            
        for date_string in important_date_strings:
            try:
                dt = parser.parse(date_string)
                ts = int(dt.timestamp() * 1000)
                important_dates.add(ts)
            except Exception as e:
                self.logger_instance.error(f"{ self.class_name} - Error parsing date string '{date_string}': {e}")
                
        return list(important_dates)

    def extract_spot_pairs(self, content: str) -> (list[str], list[str]):
        spot_tickers = {f"{match[0]}/{match[1]}" for match in self.pattern_pairs.findall(content)}
        model_tickers = [self._converter_str_to_model_ticker.convert(ticker_str=x, type=EnumCurrencyType.SPOT) \
                                                                                           for x in spot_tickers]

        high_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority == EnumPriority.HIGH.name]
        low_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority != EnumPriority.HIGH.name]
        
        return (high_priority_tickers, low_priority_tickers)
        
    def extract_usdm_pairs(self, content: str) -> (list[str], list[str]):
        matches = self.pattern_contract_pairs.findall(content)
        usdm_tickers = {f"{base}/USDT" for match in matches for base in self.pattern_base_quote.findall(match)}
        model_tickers = [self._converter_str_to_model_ticker.convert(ticker_str=x, type=EnumCurrencyType.SPOT) \
                                                                                                  for x in usdm_tickers]
        
        # Step 4: Categorize into high_priority_tickers and low_priority_tickers
        high_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority == EnumPriority.HIGH.name]
        low_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority != EnumPriority.HIGH.name]

        return (high_priority_tickers, low_priority_tickers)
    
    def extract_network_token(self, content: str, 
                                   alert_category :Union[EnumLowAlertWarningKeyWords,        
                                                        EnumHighAlertWarningKeyWords]) -> list[str]:
        
        if alert_category.value in ['contract']:
            matches = self.pattern_contract_swap.findall(content)
        else:
            matches = self.pattern_network_upgrade.findall(content)
        unique_networks = list(set(matches))
        return unique_networks
    
    def extract_trading_status(self, content: str,  
                                      alert_category :Union[EnumLowAlertWarningKeyWords,        
                                                            EnumHighAlertWarningKeyWords]) -> bool:
        
        if alert_category.value not in ['hard', 'fork', 'upgrade', 'contract']:
            return False
        
        match_1 = re.search(self.pattern_trading_not_affected, content, re.I)
        match_2 = re.search(self.pattern_trading_affected , content, re.I)
        
        if match_1 and match_2:
            return True
        if match_1:
            return False
        if match_2:
            return True
        else: 
            return False
    
        