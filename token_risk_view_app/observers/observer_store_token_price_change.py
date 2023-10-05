from typing import Optional
from datetime import timedelta, datetime
from singleton_decorator import singleton

from ews_app.enum.enum_high_alert_warning_key_words import \
                                EnumHighAlertWarningKeyWords
from token_risk_view_app.decorators.decorator_base_trading_urls import \
                                                       base_trading_urls
from ews_app.observer_interfaces.observer_interface import ObserverInterface
from token_risk_view_app.model.model_token_volatility_event import ModelTokenVolatilityEvent
from token_risk_view_app.store.stores_token_risk_view import StoreTokenRiskView
from token_risk_view_app.converters.converter_dict_to_model_token_volatility_event import \
                                                   ConverterDictToModelTokenVolatilityEvent


@singleton
class ObserverStoreTokenPriceChange(ObserverInterface):
    
    @base_trading_urls
    def __init__(self,
                 coinmarketcap_base_url,
                 **kwargs) -> None:
        super().__init__()
        StoreTokenRiskView.store_token_price_change.attach(self)
        self._coinmarketcap_base_url  = coinmarketcap_base_url
        self.converter_volatility_event = ConverterDictToModelTokenVolatilityEvent()
        
    def update(self,
               volatility_events: Optional[list]):
        
        url = self._coinmarketcap_base_url
        
        events = []
        for increment, orderbooks_dict in volatility_events.items():
            
            if len(orderbooks_dict) == 0:
                continue
            
            symbols = list(orderbooks_dict.keys())
            orderbook_last = list(orderbooks_dict.values())[-1]
            timestamp = orderbook_last.bid.timestamp  
            pretty_date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%M:%H %d:%m;%y')
        
            pretty_increment = increment.replace('_',' ').lower().title()
            title = f"{pretty_increment} Token Volatilty {pretty_date}"
            alert_category = EnumHighAlertWarningKeyWords.TOKEN_PRICE_VOLATILITY
            event_lifetime = int(timestamp+(timedelta(hours=24).total_seconds() * 1000))
            important_dates = [timestamp, event_lifetime]
                
            token_volatility_event = \
                self.converter_volatility_event.convert(
                url = url, 
                title = title, 
                release_date = timestamp,
                important_dates = important_dates, 
                alert_category = alert_category,
                h_spot_tickers = symbols
            )
            
            events.append(token_volatility_event)  
       
        return events     
        # ModelTokenVolatilityEvent.objects.filter(id__in=[x.id for x in events]).values_list('id', flat=True)