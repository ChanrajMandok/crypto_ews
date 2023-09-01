import re

from typing import Union
from dateutil import parser
from bs4 import BeautifulSoup

from binance_ews_app.services import logger
from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_currency_type import EnumCurrencyType
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.enum.enum_low_alert_warning_key_words import \
                                EnumLowAlertWarningKeyWords
from ews_app.converters.converter_str_to_model_ticker import \
                                         ConverterStrToModelTicker
from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency
from binance_ews_app.model.model_binance_article import ModelBinanceArticle
from binance_ews_app.converters.converter_model_article_to_model_event import \
                                               ConverterModelArticleToModelEvent


class ServiceBinanceArticleHtmlHandler:
    """
    Service extracts important Dates, articles, trading pairs, 
    and specific contract trading pairs from HTML format.
    """

    def __init__(self):
        self.__converter_str_to_model_ticker = ConverterStrToModelTicker()
        self.__pairs_pattern = re.compile(r"([A-Z0-9]{3,10})\/([A-Z0-9]{3,10})")
        self.__date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?)")
        self.__network_upgrade_pattern = re.compile(r"\(([A-Z0-9]{1,10})\) network")
        self.__contract_swap_pattern = re.compile(r"\(([A-Z0-9]{1,10})\) contract swap")
        self.__converter_model_article_to_model_event = ConverterModelArticleToModelEvent()
        self.__contract_pairs_pattern = \
            re.compile(r"USDⓈ-M ((?:[A-Z0-9]{1,10}[A-Z0-9]{1,10}(?: and )?)+) Perpetual Contract")

    def handle(self, article: ModelBinanceArticle) -> ModelBinanceEvent:

        try:
            release_date_ts = article.raw_article.release_date
            category = article.alert_category

            article_content_text = self.extract_article_content(article.html)
            

            h_spot_tickers, l_spot_tickers = self.extract_spot_pairs(article_content_text)
            h_usdm_tickers, l_usdm_tickers = self.extract_usdm_pairs(article_content_text)

            important_dates = self.extract_important_dates(content=article_content_text,
                                                           release_date=release_date_ts)
            trading_affected = self.extract_trading_status(content=article_content_text,
                                                            alert_category=category)
            network_tokens = self.extract_network_token(content=article_content_text,
                                                            alert_category=category)
            wx_ccy_affected = any(ModelWirexSpotCurrency.objects.filter(currency=x).exists() \
                                                                            for x in network_tokens)
            
            if (h_spot_tickers or h_usdm_tickers) or \
                (category.value in ['hard', 'fork', 'upgrade', 'contract'] \
                                    and trading_affected and wx_ccy_affected):
                article.alert_priority = EnumPriority.HIGH
            
            event = self.__converter_model_article_to_model_event.convert(
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
            logger.error(f"{self.__class__.__name__} - Unexpected error: {str(e)}\
                                        for article: {article.raw_article.title}")

    def extract_article_content(self, article_html_content: str) -> str:
        soup = BeautifulSoup(article_html_content, 'html.parser')
        target_div = soup.find("div", {"id": "support_article"})
        
        # Replace <li> elements with the text followed by a unique separator
        for li in target_div.find_all("li"):
            li.string = li.get_text() + " "
            
        if not target_div:
            logger.error(f"{self.__class__.__name__} - Unable to find target div in HTML content")
            return ''
            
        content_with_separators = target_div.get_text().strip()
        
        return content_with_separators

    def extract_important_dates(self, content: str, release_date: int) -> list[int]:
        important_date_strings = [match for match in self.__date_pattern.findall(content)]
        
        # Initialize the set with the release_date
        important_dates = {release_date}
        
        for date_string in important_date_strings:
            try:
                dt = parser.parse(date_string)
                ts = int(dt.timestamp() * 1000)
                important_dates.add(ts)
            except Exception as e:
                logger.error(f"{self.__class__.__name__} - {e}")
            
        return list(important_dates)
    
    def extract_spot_pairs(self, content: str) -> (list[str], list[str]):
        spot_tickers = {f"{match[0]}/{match[1]}" for match in self.__pairs_pattern.findall(content)}
        model_tickers = [self.__converter_str_to_model_ticker.convert(ticker_str=x, type=EnumCurrencyType.SPOT) \
                                                                                           for x in spot_tickers]

        high_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority == EnumPriority.HIGH]
        low_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority != EnumPriority.HIGH]
        
        return (high_priority_tickers, low_priority_tickers)
        
    def extract_usdm_pairs(self, content: str) -> (list[str], list[str]):
        matches = self.__contract_pairs_pattern.findall(content)
        base_quote_pattern = re.compile(r"([A-Z0-9]{1,10})USDT")
        usdm_tickers = {f"{base}/USDT" for match in matches for base in base_quote_pattern.findall(match)}
        model_tickers = [self.__converter_str_to_model_ticker.convert(ticker_str=x, type=EnumCurrencyType.SPOT) \
                                                                                                  for x in usdm_tickers]
        
        # Step 4: Categorize into high_priority_tickers and low_priority_tickers
        high_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority == EnumPriority.HIGH]
        low_priority_tickers = [ticker.name for ticker in model_tickers if ticker.alert_priority != EnumPriority.HIGH]

        return (high_priority_tickers, low_priority_tickers)
    
    def extract_network_token(self, content: str, 
                                   alert_category :Union[EnumLowAlertWarningKeyWords,        
                                                        EnumHighAlertWarningKeyWords]) -> list[str]:
        
        if alert_category.value in ['contract']:
            matches = self.__contract_swap_pattern.findall(content)
        else:
            matches = self.__network_upgrade_pattern.findall(content)
        unique_networks = list(set(matches))
        return unique_networks
    
    def extract_trading_status(self, content: str,  
                                      alert_category :Union[EnumLowAlertWarningKeyWords,        
                                                            EnumHighAlertWarningKeyWords]) -> bool:
        
        if alert_category.value not in ['hard', 'fork', 'upgrade', 'contract']:
            return False
        
        pattern_1 = r'The trading of ((?:\w+\s?){1,5}) will not be affected during'
        match_1 = re.search(pattern_1, content, re.I)

        pattern_2 = r'deposits and withdrawals of ((?:\w+\s?){1,8}) will be suspended'
        match_2 = re.search(pattern_2, content, re.I)
        
        if match_1 and match_2:
            return True
        if match_1:
            return False
        if match_2:
            return True
        else: 
            return False
    
        