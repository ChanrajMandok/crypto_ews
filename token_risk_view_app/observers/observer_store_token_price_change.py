from typing import Optional
from singleton_decorator import singleton

from ews_app.observer_interfaces.observer_interface import ObserverInterface
from token_risk_view_app.store.stores_token_risk_view import StoreTokenRiskView

@singleton
class ObserverStoreTokenPriceChange(ObserverInterface):
    
    def __init__(self) -> None:
        super().__init__()
        StoreTokenRiskView.store_token_price_change.attach(self)
        
    def update(self,
               accumulated_updates: Optional[list]):
        
        for value in accumulated_updates:
            print(value) 
        
        