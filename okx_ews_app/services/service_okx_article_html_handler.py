import re

from singleton_decorator import singleton

from okx_ews_app.services import logger
from ews_app.enum.enum_source import EnumSource
from okx_ews_app.converters.converter_okx_article_to_okx_event import \
                                          ConverterOkxArticleToOkxEvent
from ews_app.service_interfaces.service_model_article_html_handler_interface import \
                                              ServiceModelArticleHtmlHandlerInterface


@singleton
class ServiceOkxArticleHtmlHandler(ServiceModelArticleHtmlHandlerInterface):
    """
    Service extracts important Dates, articles, trading pairs, 
    and specific contract trading pairs from HTML format.
    """
    
    def __init__(self):
        super().__init__()
        self._logger_instance = logger
        self._pattern_base_quote = re.compile(r"([A-Z0-9]{1,10})USDT")
        self._pairs_pattern = re.compile(r"([A-Z0-9]{3,10})(?:\/|-)([A-Z0-9]{3,10})")
        self._network_upgrade_pattern = re.compile(r"\(([A-Z0-9]{1,10})\) network")
        self._contract_swap_pattern = re.compile(r"\(([A-Z0-9]{1,10})\) contract swap")
        self._converter_model_article_to_model_event = ConverterOkxArticleToOkxEvent()
        self._contract_pairs_pattern = \
            re.compile(r"USDⓈ-M ((?:[A-Z0-9]{1,10}[A-Z0-9]{1,10}(?: and )?)+) Perpetual Contract")
        self._pattern_trading_not_affected = r'The trading of ((?:\w+\s?){1,5}) will not be affected '
        self._pattern_trading_affected = \
            (r'(transfers(, deposits)?(, and withdrawals)?|deposits(, and withdrawals)?|withdrawals) will be suspended')
        self._date_pattern = \
           re.compile(r'\d{1,2}:\d{2} [apAP][mM] UTC on \w+ \d{1,2}, \d{4}|\w+ \d{1,2}, \d{4}(?:, \d{1,2}:\d{2} [apAP][mM] UTC)?|\w+ \d{1,2}, \d{4}(?:, \d{1,2}:\d{2} - \d{1,2}:\d{2} [apAP][mM] UTC)?')
        
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
        
    @property
    def pattern_pairs(self) -> str:
        return self._pairs_pattern
        
    @property
    def pattern_date(self):
        return self._date_pattern
    
    @property
    def pattern_network_upgrade(self):
        return self._network_upgrade_pattern
    
    @property
    def pattern_contract_swap(self):
        return self._contract_swap_pattern

    @property
    def pattern_contract_pairs(self):
        return self._contract_pairs_pattern
    
    @property
    def pattern_base_quote(self):
        return self._pattern_base_quote

    @property
    def pattern_trading_not_affected(self):
        return self._pattern_trading_not_affected
    
    @property
    def pattern_trading_affected(self):
        return self._pattern_trading_affected
    
    def converter_a_to_e(self):
        return self._converter_model_article_to_model_event
    
    def source(self):
        return EnumSource.OKX