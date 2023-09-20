from django.test import TestCase

from defi_llama_ews_app.model.model_defi_stablecoin import \
                                          ModelDefiStablecoin
from defi_llama_ews_app.model.model_defi_llama_bridge_hack import \
                                            ModelDefiLlamaBridgeHack
from defi_llama_ews_app.services.service_defi_lama_url_retriever import \
                                                ServiceDefiLamaUrlRetriever
from defi_llama_ews_app.model.model_defi_llama_hack import ModelDefiLlamaHack
from defi_llama_ews_app.services.service_defi_llama_model_hack_retriever import \
                                                ServiceDefiLlamaModelHackRetriever
from defi_llama_ews_app.services.service_defi_llama_bridge_hack_retriever import \
                                                ServiceDefiLlamaBridgeHackRetriever
from defi_llama_ews_app.services.service_defi_llama_model_stablecoin_retriever import \
                                                ServiceDefiLlamaModelStablecoinRetriever
from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv
from ews_app.tasks.task_populate_stablecoins_from_env import TaskPopulateWirexStableCoinsFromEnv


class TestDefiLlamaServicesTestCase(TestCase):

    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        TaskPopulateWirexStableCoinsFromEnv().populate()
        self.__service_defi_lama_url_retriever = ServiceDefiLamaUrlRetriever()
        self.__service_defi_llama_model_hack_retriever = ServiceDefiLlamaModelHackRetriever()
        self.__service_defi_llama_bridge_hack_retriever = ServiceDefiLlamaBridgeHackRetriever()
        self.__service_defi_llama_model_stablecoin_retriever = ServiceDefiLlamaModelStablecoinRetriever()

    def test_service_defi_lama_url_retriever(self):

        url = self.__service_defi_lama_url_retriever.retrieve(endpoint='hacks.json')
        self.assertIsNotNone(url)

    def test_service_defi_llama_bridge_hack_retriever(self):

        model_bridge_hack_list = self.__service_defi_llama_bridge_hack_retriever.retrieve(test=True)

        self.assertIsNotNone(model_bridge_hack_list)
        self.assertTrue(isinstance(model_bridge_hack_list[-1], ModelDefiLlamaBridgeHack))

    def test_service_defi_llama_model_stablecoin_retriever(self):

        model_stablecoin_list = self.__service_defi_llama_model_stablecoin_retriever.retrieve(test=True)

        self.assertIsNotNone(model_stablecoin_list)
        self.assertTrue(isinstance(model_stablecoin_list[-1], ModelDefiStablecoin))

    def test_service_defi_llama_model_hack_retriever(self):

        model_hack_list = self.__service_defi_llama_model_hack_retriever.retrieve(test=True)

        self.assertIsNotNone(model_hack_list)
        self.assertTrue(isinstance(model_hack_list[-1], ModelDefiLlamaHack))