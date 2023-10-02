from ews_app.store.store_interface import StoreInterface
from ews_app.model.model_order_book import ModelOrderBook
from token_risk_view_app.enum.enum_orderbook_updated_increment import \
                                          EnumOrderbookUpdatedIncrement


class StoreTokenRiskView():
    
    one_minute_price_store          = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()
    fifteen_minutes_price_store     = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()
    thirty_minutes_price_store      = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()
    one_hour_price_store            = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()
    six_hours_price_store           = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()
    twelve_hours_price_store        = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()
    twenty_four_hours_price_store   = StoreInterface[EnumOrderbookUpdatedIncrement.choices, ModelOrderBook]()