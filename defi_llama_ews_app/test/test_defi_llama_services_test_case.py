from django.test import TestCase

from defi_llama_ews_app.services.service_defi_lama_url_retriever import \
                                                ServiceDefiLamaUrlRetriever
from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv
from ews_app.tasks.task_populate_stablecoins_from_env import TaskPopulateWirexStableCoinsFromEnv


class TestDefiLlamaConvertersTestCase(TestCase):

    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        TaskPopulateWirexStableCoinsFromEnv().populate()
        self.__service_defi_lama_url_retriever = ServiceDefiLamaUrlRetriever()

    def test_service_defi_lama_url_retriever(self):

        url = self.__service_defi_lama_url_retriever.retrieve(endpoint='hacks.json')
        self.assertIsNotNone(url)

    