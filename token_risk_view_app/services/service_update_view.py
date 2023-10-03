from ews_app.enum.enum_source import EnumSource
from token_risk_view_app.services.service_store_update_manager import \
                                              ServiceStoreUpdateManager
from ews_app.service_interfaces.service_orderbook_retriever_interface import \
                                            ServiceOrderBookRetrieverInterface 


class ServiceUpdateVeiw:
    
    def __init__(self) -> None:
        self.service_store_update_manager = ServiceStoreUpdateManager()

    def update_store(self) -> None:
        
        final_data = {}
        for cls in ServiceOrderBookRetrieverInterface.__subclasses__():
            retrieved_data = cls().retrieve()

            for key, value in retrieved_data.items():
                if value.source == EnumSource.BINANCE:
                    # Prioritize Binance data
                    final_data[key] = value
                elif value.source == EnumSource.OKX and key not in final_data:
                    # OKX is Backup Data
                    final_data[key] = value
        
        self.service_store_update_manager.update_stores(orderbooks=final_data)