import json

from datetime import datetime
from django.test import TestCase

from ews_app.enum.enum_source import EnumSource
from ews_app.enum.enum_priority import EnumPriority
from defi_llama_ews_app.model.model_defi_llama_bridge_hack import \
                                            ModelDefiLlamaBridgeHack
from ews_app.model.model_wirex_stablecoin import ModelWirexStableCoin
from defi_llama_ews_app.model.model_defi_hack_event import ModelDefiHackEvent
from defi_llama_ews_app.model.model_defi_llama_hack import ModelDefiLlamaHack
from defi_llama_ews_app.model.model_defi_stablecoin import ModelDefiStablecoin
from defi_llama_ews_app.converters.converter_dict_to_model_stablecoin import \
                                        ConverterDefiLlamaDictToModelStableCoin
from defi_llama_ews_app.converters.converter_dict_to_model_bridge_hack import \
                                                  ConverterDictToModelBridgeHack
from defi_llama_ews_app.converters.convert_model_stablecoin_to_model_event import \
                                                 ConvertModelStablecoinToModelEvent
from defi_llama_ews_app.converters.converter_defi_llama_list_to_model_hack import \
                                                    ConverterDefiLlamaListToModelHack
from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords
from ews_app.tasks.task_populate_currencies_from_env import TaskPopulateCurrenciesFromEnv
from defi_llama_ews_app.model.model_defi_stablecoin_event import ModelDefiStableCoinEvent
from defi_llama_ews_app.converters.converter_model_defi_llama_hack_to_model_event import \
                                                        ConverterModelDefiHackToModelEvent
from defi_llama_ews_app.model.model_defi_bridge_hack_event import ModelDefiBridgeHackEvent
from defi_llama_ews_app.converters.converter_model_defi_bridge_hack_to_model_event import \
                                                    ConverterModelDefiBridgeHackToModelEvent
from ews_app.tasks.task_populate_stablecoins_from_env import TaskPopulateWirexStableCoinsFromEnv


class TestDefiLlamaConvertersTestCase(TestCase):

    def setUp(self):
        TaskPopulateCurrenciesFromEnv().populate()
        TaskPopulateWirexStableCoinsFromEnv().populate()
        self.converter_dict_to_model_bridge_hack                = ConverterDictToModelBridgeHack()
        self.converter_defi_llama_list_to_model_hack            = ConverterDefiLlamaListToModelHack()
        self.convert_model_stablecoin_to_model_event            = ConvertModelStablecoinToModelEvent()
        self.converter_model_defi_llama_hack_to_model_event     = ConverterModelDefiHackToModelEvent()
        self.converter_dict_to_model_stablecoin                 = ConverterDefiLlamaDictToModelStableCoin()
        self.converter_model_defi_bridge_hack_to_model_event    = ConverterModelDefiBridgeHackToModelEvent()

    def test_converter_dict_to_model_defi_bridge_hack_interface(self):

        filepath = r'./defi_llama_ews_app\test\data\bridge_hack_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        model_defi_bridge_hack = self.converter_dict_to_model_bridge_hack.convert(defi_llama_dict=data_dict)

        self.assertIsNotNone(model_defi_bridge_hack)
        self.assertTrue(isinstance(model_defi_bridge_hack, ModelDefiLlamaBridgeHack))

    def test_converter_dict_to_model_stablecoin(self):

        filepath = r'./defi_llama_ews_app\test\data\stablecoin_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        model_stablecoin = \
            self.converter_dict_to_model_stablecoin.convert(
                        dict = data_dict,
                        trading_affected = True,
                        alert_priority = EnumPriority.HIGH,
                        alert_category = EnumHighAlertWarningKeyWords.DEPEG,
                        url = 'https://www.defi.com/en/support/announcement/testing_exmaple'
                                                            )

        self.assertIsNotNone(model_stablecoin)
        self.assertTrue(isinstance(model_stablecoin, ModelDefiStablecoin))

    def test_converter_defi_llama_list_to_model_hack(self):

        filepath = r'./defi_llama_ews_app\test\data\hack_list.json'
        with open(filepath, "r") as f:
            data_list = json.loads(f.read())

        model_hack = self.converter_defi_llama_list_to_model_hack.convert(data_list)

        self.assertIsNotNone(model_hack)
        self.assertTrue(isinstance(model_hack, ModelDefiLlamaHack))

    def test_convert_model_stablecoin_to_model_event(self):

        filepath = r'./defi_llama_ews_app\test\data\stablecoin_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        source = EnumSource.DEFI_LLAMA
        now = int(datetime.now().timestamp()) * 1000

        wx_stablecoin = ModelWirexStableCoin.objects.get(currency=data_dict['symbol'])

        model_stablecoin = \
            ModelDefiStablecoin(
                                release_date         = now,
                                trading_affected     = True,
                                stablecoin           = wx_stablecoin,
                                alert_priority       = EnumPriority.HIGH,
                                price                = data_dict['price'],
                                one_day_price_change = data_dict['change_1d'],
                                mechanism            = data_dict['pegMechanism'],
                                peg_deviation        = data_dict['pegDeviation'],
                                alert_category       = EnumHighAlertWarningKeyWords.DEPEG,
                                url                  = 'https://www.defi.com/en/support/announcement/testing_exmaple')
        
        model_stablecoin_event = \
                                self.convert_model_stablecoin_to_model_event.convert(
                                    source=source,
                                    model_stablecoin=model_stablecoin
                                )

        self.assertIsNotNone(model_stablecoin_event)
        self.assertTrue(isinstance(model_stablecoin_event, ModelDefiStableCoinEvent))

    def test_converter_model_defi_llama_hack_to_model_event(self):

        filepath = r'./defi_llama_ews_app\test\data\hack_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        model_hack = ModelDefiLlamaHack(
                        trading_affected   = True,
                        url                = data_dict['url'],
                        exploit            = data_dict['exploit'],
                        protocol           = data_dict['protocol'],
                        alert_priority     = EnumPriority.HIGH.name,
                        blockchain         = data_dict['blockchain'],
                        release_date       = data_dict['release_date'],
                        network_tokens     = data_dict['network_tokens'],
                        hacked_amount_m    = data_dict['hacked_amount_m'],
                        alert_category     = EnumHighAlertWarningKeyWords.HACK,
                    )
        
        model_event = \
            self.converter_model_defi_llama_hack_to_model_event.convert(
                                                                        model_hack=model_hack,
                                                                        source = EnumSource.DEFI_LLAMA)
        

        self.assertIsNotNone(model_event)
        self.assertTrue(isinstance(model_event, ModelDefiHackEvent))


    def test_converter_model_defi_bridge_hack_to_model_event(self):

        filepath = r'./defi_llama_ews_app\test\data\hack_dict.json'
        with open(filepath, "r") as f:
            data_dict = json.loads(f.read())

        model_hack =  ModelDefiLlamaBridgeHack(
                trading_affected   = True,
                url                = data_dict['url'],
                exploit            = data_dict['exploit'],
                protocol           = data_dict['protocol'],
                alert_priority     = EnumPriority.HIGH.name,
                blockchain         = data_dict['blockchain'],
                release_date       = data_dict['release_date'],
                network_tokens     = data_dict['network_tokens'],
                hacked_amount_m    = data_dict['hacked_amount_m'],
                alert_category     = EnumHighAlertWarningKeyWords.BRIDGE_HACK
            )
        
        model_event = \
            self.converter_model_defi_bridge_hack_to_model_event.convert(
                                                                        model_hack=model_hack,
                                                                        source = EnumSource.DEFI_LLAMA
        )

        self.assertIsNotNone(model_event)
        self.assertTrue(isinstance(model_event, ModelDefiBridgeHackEvent))