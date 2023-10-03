from datetime import datetime, timedelta

from token_risk_view_app.services import logger
from ews_app.model.model_order_book import ModelOrderBook
from token_risk_view_app.enum.enum_orderbook_updated_increment import \
                                          EnumOrderbookUpdatedIncrement
from token_risk_view_app.store.stores_token_risk_view import StoreTokenRiskView


class ServiceStoreUpdateManager:
    
    def __init__(self) -> None:
         self.logger_instance = logger
         self.class_name = self.__class__.__name__
         self.store_nested_price_change = StoreTokenRiskView.store_nested_price_change
        
    def update_stores(self, 
                      orderbooks: dict[str, ModelOrderBook]):
        
        try:
            update_increments = self._determine_update_increments()
            
            if update_increments:
                self.store_nested_price_change.batch_update(
                    orderbooks=orderbooks,
                    update_increments=update_increments
                )

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: _determine_update_increments ERROR: {str(e)}")
            
        self.logger_instance.info(f"{self.class_name}: {', '.join(update_increments)} Increments Updated")

    def _determine_update_increments(self) -> list[str]:
        
        current_ts = int(datetime.now().timestamp()) * 1000
        update_increments_to_process = []

        store_updated_dict = self.store_nested_price_change.get_last_updated_timestamps()

        for update_increment, last_updated in store_updated_dict.items():
            if last_updated is None:
                # If never updated, add to list
                last_updated = current_ts - timedelta(minutes=1500).total_seconds() * 1000 
                update_increments_to_process.append(update_increment)
                continue

            time_difference = current_ts - last_updated
            expected_difference = EnumOrderbookUpdatedIncrement[update_increment].value.total_seconds() * 1000 

            if time_difference >= expected_difference:
                update_increments_to_process.append(update_increment)

        return update_increments_to_process