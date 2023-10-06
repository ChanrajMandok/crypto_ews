from datetime import datetime , timedelta

from django.test import TestCase
from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from token_risk_view_app.model.model_token_volatility_event import \
                                           ModelTokenVolatilityEvent
from token_risk_view_app.enum.enum_orderbook_updated_increment import \
                                          EnumOrderbookUpdatedIncrement
from token_risk_view_app.converters.converter_dict_to_model_token_volatility_event import \
                                                   ConverterDictToModelTokenVolatilityEvent


class TestTokenRiskViewAppAllConvertersTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        
    def test_converter_dict_to_model_token_volatility_event(self):
        
        try:
            converter_model_token_volatility_event = ConverterDictToModelTokenVolatilityEvent()
            
            timestamp = int(datetime.now().timestamp() * 1000)
            event_lifetime = int(timestamp+(timedelta(hours=24).total_seconds() * 1000))
            
            url = 'www.test.com'
            title = 'Testing ConverterDictToModelTokenVolatilityEvent'
            important_dates = [timestamp, event_lifetime]
            increment_in_seconds = int(EnumOrderbookUpdatedIncrement.ONE_MINUTE.value.total_seconds() * 1000)
            alert_category =EnumHighAlertWarningKeyWords.TOKEN_PRICE_VOLATILITY
            symbols = ['TESTUSDT', 'TESTBTC', 'TESTUSDC']
            
            token_volatility_event = \
                    converter_model_token_volatility_event .convert(
                                                                    url = url, 
                                                                    title = title, 
                                                                    release_date = timestamp,
                                                                    h_spot_tickers = symbols,
                                                                    alert_category = alert_category,
                                                                    important_dates = important_dates, 
                                                                    increment_in_seconds = increment_in_seconds
                                                                    )
                    
            self.assertIsNotNone(token_volatility_event)
            self.assertIsInstance(token_volatility_event, ModelTokenVolatilityEvent)
                
        except Exception as e:
            raise Exception(f"Failure in converter_dict_to_model_token_volatility_event: {e}")