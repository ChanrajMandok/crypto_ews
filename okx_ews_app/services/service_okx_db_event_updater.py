from singleton_decorator import singleton

from okx_ews_app.services import logger
from okx_ews_app.store.stores_okx import StoreOkx
from okx_ews_app.model.model_okx_event import ModelOkxEvent
from ews_app.services.service_send_model_event_to_ms_teams import \
                                     ServiceSendModelEventToMsTeams
from okx_ews_app.services.service_okx_raw_article_retriever import \
                                       ServiceOkxRawArticleRetriever
from okx_ews_app.services.service_okx_article_html_retriever import \
                                       ServiceOkxArticleHtmlRetriever
from ews_app.service_interfaces.service_db_event_updater_interface import \
                                             ServiceDbEventUpdaterInterface
from okx_ews_app.model.model_db_okx_last_updated import ModelDbOkxLastUpdated
from okx_ews_app.services.service_okx_raw_article_keyword_classifier import \
                                        ServiceOkxRawArticleKeywordClassifier


@singleton
class ServiceOkxDbEventUpdater(ServiceDbEventUpdaterInterface):

    def __init__(self) -> None:
        super().__init__()
        self._logger_instance = logger
        self._service_raw_article_retriever          = ServiceOkxRawArticleRetriever()
        self._service_article_html_retriever         = ServiceOkxArticleHtmlRetriever()
        self._service_send_model_event_to_ms_teams   = ServiceSendModelEventToMsTeams()
        self._store_db_okx_last_updated              = StoreOkx.store_db_okx_last_updated
        self._service_raw_article_keyword_classifier = ServiceOkxRawArticleKeywordClassifier()

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
        return self._store_db_okx_last_updated 

    def service_raw_article_keyword_classifier(self):
        return self._service_raw_article_keyword_classifier

    def model_db_last_updated(self):
        return ModelDbOkxLastUpdated

    def model_event(self):
        return ModelOkxEvent