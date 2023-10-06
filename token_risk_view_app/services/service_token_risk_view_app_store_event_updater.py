from datetime import datetime, timedelta
from ews_app.enum.enum_source import EnumSource

from token_risk_view_app.services import logger
from token_risk_view_app.enum.enum_orderbook_updated_increment import \
                                          EnumOrderbookUpdatedIncrement
from token_risk_view_app.store.stores_token_risk_view import StoreTokenRiskView
from ews_app.service_interfaces.service_orderbook_retriever_interface import \
                                            ServiceOrderBookRetrieverInterface 


class ServiceStoreEventUpdater:
    
    def __init__(self) -> None:
        self.logger_instance = logger
        self.class_name = self.__class__.__name__
        self.store_nested_price_change = StoreTokenRiskView.store_token_price_change
        
    def update_store(self):
        try:
            orderbooks = self._retrieve_orderbooks()
            update_increments = self._determine_update_increments()

            if update_increments:
                self.store_nested_price_change.set_instances(
                    orderbooks=orderbooks,
                    update_increments=update_increments
                )
                self.logger_instance.info(f"{self.class_name}: {', '.join(update_increments)} Increments Updated")
            else:
                self.logger_instance.info(f"{self.class_name}: No increments to update")

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: update_store ERROR: {str(e)}")

    def _retrieve_orderbooks(self) -> dict:
        orderbooks = {}
        for cls in ServiceOrderBookRetrieverInterface.__subclasses__():
            try:
                retrieved_data = cls().retrieve()

                for key, value in retrieved_data.items():
                    if value.source == EnumSource.BINANCE:
                        # Prioritize Binance data
                        orderbooks[key] = value
                    elif value.source == EnumSource.OKX and key not in orderbooks:
                        # OKX is Backup Data
                        orderbooks[key] = value

            except Exception as e:
                self.logger_instance.error(f"{self.class_name}: _retrieve_orderbooks for {cls} ERROR: {str(e)}")

        return orderbooks

    def _determine_update_increments(self) -> list[str]:
        current_ts = int(datetime.now().timestamp()) * 1000
        update_increments_to_process = []

        try:
            store_updated_dict = self.store_nested_price_change.get_last_updated_timestamps()

            for update_increment, last_updated in store_updated_dict.items():
                if last_updated is None:
                    # If never updated, add to list
                    update_increments_to_process.append(update_increment)
                    continue

                time_difference = current_ts - last_updated
                expected_difference = int(EnumOrderbookUpdatedIncrement[update_increment].value.total_seconds() * 1000) 
                if not expected_difference:
                    continue

                if time_difference >= expected_difference:
                    update_increments_to_process.append(update_increment)

        except Exception as e:
            self.logger_instance.error(f"{self.class_name}: _determine_update_increments ERROR: {str(e)}")

        return update_increments_to_process