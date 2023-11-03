from ews_app.model.model_order_book import ModelOrderBook
from token_risk_view_app.enum.enum_orderbook_updated_increment import \
                                          EnumOrderbookUpdatedIncrement
from token_risk_view_app.store.store_token_price_change_interface import \
                                            StoreTokenPriceChangeInterface


class StoreTokenRiskView():
    
    update_increments = [x.name for x in EnumOrderbookUpdatedIncrement]
    store_token_price_change = StoreTokenPriceChangeInterface[str, ModelOrderBook](update_increments=update_increments)