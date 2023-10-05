from singleton_decorator import singleton

from ews_app.services import logger
from ews_app.services.service_wx_analytics_connection_retriever import \
                                   ServiceWxAnalyticsConnectionRetriever
from ews_app.model.model_wirex_spot_currency import ModelWirexSpotCurrency


@singleton
class ServiceWxAnalyticsCurrenciesRetriever:

    def __init__(self):
        self.currencies = None
        self.config_wirex_data_connect = ServiceWxAnalyticsConnectionRetriever()

    def _create_currency_from_row(self, row):
        return ModelWirexSpotCurrency(
            id=row[0],
            currency=row[1],
        )

    def query_currencies(self):
        sql = "SELECT * FROM dbo.__DICT__CurrencyName"
        
        with self.config_wirex_data_connect.get_wirex_pyodbc_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

            self.currencies = [self._create_currency_from_row(row) for row in cursor.fetchall() if row[2] =='Crypto']

        logger.info("currencies data query completed.")

    def get_currencies(self) -> list[ModelWirexSpotCurrency]:
        if self.currencies is None:
            self.query_currencies()
        return self.currencies
