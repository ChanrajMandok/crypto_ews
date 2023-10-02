from singleton_decorator import singleton

from binance_ews_app.services import logger
from binance_ews_app.store.stores_binance import StoreBinance
from binance_ews_app.model.model_db_binance_last_updated import \
                                        ModelDbBinanceLastUpdated
from ews_app.services.service_send_model_event_to_ms_teams import \
                                     ServiceSendModelEventToMsTeams
from binance_ews_app.model.model_binance_event import ModelBinanceEvent
from ews_app.service_interfaces.service_db_event_updater_interface import \
                                             ServiceDbEventUpdaterInterface
from binance_ews_app.services.service_binance_raw_article_retriever import \
                                           ServiceBinanceRawArticleRetriever
from binance_ews_app.services.service_binance_article_html_retriever import \
                                           ServiceBinanceArticleHtmlRetriever
from binance_ews_app.services.service_binance_raw_article_keyword_classifier import \
                                            ServiceBinanceRawArticleKeywordClassifier


@singleton
class ServiceBinanceDbEventUpdater(ServiceDbEventUpdaterInterface):

    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_raw_article_retriever          = ServiceBinanceRawArticleRetriever()
        self._service_article_html_retriever         = ServiceBinanceArticleHtmlRetriever()
        self._service_send_model_event_to_ms_teams   = ServiceSendModelEventToMsTeams()
        self._store_db_binance_last_updated          = StoreBinance.store_db_binance_last_updated
        self._service_raw_article_keyword_classifier = ServiceBinanceRawArticleKeywordClassifier()

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    def service_raw_article_retriever(self):
        return self._service_raw_article_retriever

    def service_article_html_retriever(self):
        return self._service_article_html_retriever

    def service_send_model_event_to_ms_teams(self):
        return self._service_send_model_event_to_ms_teams

    def store_db_last_updated(self):
        return self._store_db_binance_last_updated 

    def service_raw_article_keyword_classifier(self):
        return self._service_raw_article_keyword_classifier

    def model_db_last_updated(self):
        return ModelDbBinanceLastUpdated

    def model_event(self):
        return ModelBinanceEvent