from django.test import TestCase

from ews_app.decorators.decorator_refresh_increments import \
                                 decorator_refresh_increments
from okx_ews_app.decorators.decorator_okx_headers_required import \
                                               okx_headers_required
from ews_app.decorators.decorator_orderbooks_urls_required import \
                                           orderbooks_urls_required
from ews_app.decorators.decorator_tickers_spot_list_required import \
                                           spot_tickers_list_required
from binance_ews_app.decorators.decorator_binance_urls_required import \
                                                    binance_url_required
from ews_app.decorators.decorator_base_trading_urls import base_trading_urls
from binance_ews_app.decorators.decorator_binance_headers_required import \
                                                   binance_headers_required
from ews_app.decorators.decorator_webhook_urls import webhooks_urls_required
from defi_llama_ews_app.decorators.decorator_defi_llama_urls_required import \
                                                      defi_llama_urls_required
from okx_ews_app.decorators.decorator_okx_urls_required import okx_url_required
from defi_llama_ews_app.decorators.decorator_defi_llama_headers_required import \
                                                      defi_llama_headers_required
from defi_llama_ews_app.decorators.decorator_defi_llama_json_headers_required import \
                                                      defi_llama_json_headers_required


class TestAllDecoratorsTestCase(TestCase):

    @binance_url_required
    @binance_headers_required
    def test_decorators_binance_ews_app(self,                               
                                        binance_headers,
                                        binance_delist_url,
                                        binance_news_dict_url,
                                        binance_delist_headers,
                                        binance_article_base_url,
                                        **kwargs):
        
        self.assertIsNotNone(binance_headers)
        self.assertIsNotNone(binance_delist_url)
        self.assertIsNotNone(binance_news_dict_url)
        self.assertIsNotNone(binance_delist_headers)
        self.assertIsNotNone(binance_article_base_url)

    @defi_llama_urls_required
    @defi_llama_headers_required
    @defi_llama_json_headers_required
    def test_decorators_defi_llama_ews_app(self,
                                           defi_llama_headers,
                                           defi_llama_base_url,
                                           defi_llama_hacks_url,
                                           defi_llama_json_headers,
                                           **kwargs):
        
        self.assertIsNotNone(defi_llama_headers)
        self.assertIsNotNone(defi_llama_base_url)
        self.assertIsNotNone(defi_llama_hacks_url)
        self.assertIsNotNone(defi_llama_json_headers)
        
    @base_trading_urls
    @webhooks_urls_required
    @orderbooks_urls_required
    @spot_tickers_list_required
    @decorator_refresh_increments
    def test_decorators_ews_app(self,
                                base_ccys,
                                cex_webhook,
                                defi_webhook,
                                token_webhook,
                                stablecoin_webhook,
                                token_liquidity_webhook,
                                okx_orderbooks_url,
                                binance_orderbooks_url, 
                                raw_tickers_spot_list,
                                coinmarketcap_base_url,
                                update_refresh_increment_mins,
                                manager_refresh_increment_mins,
                                tickers_spot_list_okx_format,
                                orderbooks_refresh_increment_mins,
                                defi_llama_refresh_increment_mins,
                                tickers_spot_list_binance_format,
                                **kwargs):
        
        self.assertIsNotNone(base_ccys)
        self.assertIsNotNone(cex_webhook)
        self.assertIsNotNone(defi_webhook)
        self.assertIsNotNone(token_webhook)
        self.assertIsNotNone(okx_orderbooks_url)
        self.assertIsNotNone(stablecoin_webhook)
        self.assertIsNotNone(raw_tickers_spot_list)
        self.assertIsNotNone(coinmarketcap_base_url)
        self.assertIsNotNone(binance_orderbooks_url)
        self.assertIsNotNone(token_liquidity_webhook)
        self.assertIsNotNone(update_refresh_increment_mins)
        self.assertIsNotNone(manager_refresh_increment_mins)
        self.assertIsNotNone(tickers_spot_list_okx_format)
        self.assertIsNotNone(orderbooks_refresh_increment_mins)
        self.assertIsNotNone(defi_llama_refresh_increment_mins)
        self.assertIsNotNone(tickers_spot_list_binance_format)

    @okx_url_required
    @okx_headers_required
    def test_decorators_okx_ews_app(self,
                                    okx_headers,
                                    okx_delist_url,
                                    okx_news_dict_url,
                                    okx_article_base_url,
                                    **kwargs):
        
        self.assertIsNotNone(okx_headers)
        self.assertIsNotNone(okx_delist_url)
        self.assertIsNotNone(okx_news_dict_url)
        self.assertIsNotNone(okx_article_base_url)
