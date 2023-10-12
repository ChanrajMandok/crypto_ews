from datetime import datetime

from django.test import TestCase
from ews_app.model.model_order_book import ModelOrderBook
from ews_app.tasks.task_populate_currencies_from_env import \
                                TaskPopulateCurrenciesFromEnv
from token_risk_view_app.enum.enum_warning_price_change import \
                                          EnumWarningPriceChange
from token_risk_view_app.services.service_token_risk_view_app_store_event_updater import \
                                              ServiceStoreEventUpdater
from token_risk_view_app.store.stores_token_risk_view import StoreTokenRiskView         
                                            
                                            
class TestTokenRiskViewAppAllServicesTestCase(TestCase):
    
    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        
    def test_service_store_event_updater(self):
        try:
            service_store_event_updater = ServiceStoreEventUpdater()
            service_store_event_updater.update_store()
            
            store_token_price_change_interface = StoreTokenRiskView.store_token_price_change
            last_updates = store_token_price_change_interface.get_last_updated_timestamps().values()
            store_data = store_token_price_change_interface.data
            now = datetime.now().timestamp() * 1000
            one_minute_in_milliseconds = 60 * 1000
            # check store has been updated 
            self.assertIsNotNone(last_updates)
            #check that the dictionary object of the storre ins not open 
            self.assertIsNotNone(store_data)
            # check update timestamp is within 1 min boundry
            for timestamp in last_updates:
                difference = abs(now - timestamp)
                self.assertLessEqual(difference, one_minute_in_milliseconds)
            
            btcusdt_orderbook = store_data[EnumWarningPriceChange.ONE_MINUTE.name]['data']['BTC/USDT']
            orderbook_updated_timestamp = btcusdt_orderbook.bid.timestamp
            self.assertIsInstance(btcusdt_orderbook, ModelOrderBook)
            difference = abs(now - orderbook_updated_timestamp)
            self.assertLessEqual(difference, one_minute_in_milliseconds)
            
        except Exception as e:
            raise Exception(f"Failure in service_store_event_updater: {e}")