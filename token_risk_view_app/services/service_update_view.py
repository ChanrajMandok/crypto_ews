from ews_app.enum.enum_source import EnumSource

from ews_app.service_interfaces.service_orderbook_retriever_interface import ServiceOrderBookRetrieverInterface


class ServiceUpdateVeiw():

    def update_store(self) -> None:
        
        final_data = {}
        retrieved_data = {}
        for cls in ServiceOrderBookRetrieverInterface.__subclasses__():
            retrieved_data = cls().retrieve()
            
            for key, value in retrieved_data.items():
                if value.source == EnumSource.BINANCE:
                    # Prioritise Binance data
                    final_data[key] = value
                elif value.source == EnumSource.OKX and key not in final_data:
                    # OKX is Backup Data
                    final_data[key] = value
