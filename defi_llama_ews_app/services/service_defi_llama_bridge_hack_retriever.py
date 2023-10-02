from datetime import datetime
from singleton_decorator import singleton

from defi_llama_ews_app.services import logger
from defi_llama_ews_app.converters.converter_dict_to_model_bridge_hack import \
                                                 ConverterDictToModelBridgeHack
from defi_llama_ews_app.decorator.decorator_defi_llama_json_headers_required import \
                                                     defi_llama_json_headers_required
from defi_llama_ews_app.service_interfaces.service_defi_llama_json_retriever_interface import \
                                                         ServiceDefiLlamaJsonRetrieverInterface


@singleton
class ServiceDefiLlamaBridgeHackRetriever(ServiceDefiLlamaJsonRetrieverInterface):
      
    @defi_llama_json_headers_required
    def __init__(self, 
                 defi_lama_json_headers) -> None:
        super().__init__()
        self._logger_instance     = logger
        self._headers             = defi_lama_json_headers
        self._converter           = ConverterDictToModelBridgeHack()

    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def url_headers(self):
        return self._headers
    
    @property
    def url_json(self):
        return 'hacks.json'
    
    @property
    def intial_key(self):
        return 'pageProps'
    
    @property
    def second_key(self):
        return 'data'
    
    def filter_results(self, object_list, test: bool = False):
        if test:
            return object_list
        
        now = int(datetime.now().timestamp()) - int(259200)
        filtered_objects =  [x for x in object_list if int(x['date']) >= now and x['bridge'] == True] 
        return filtered_objects
    
    def retrieve(self, test: bool = False):
        bridge_hack_objects = super().retrieve(test=test)
        model_objects = []
        if bridge_hack_objects:
            for value in bridge_hack_objects:
                obj = self._converter.convert(defi_llama_dict=value)
                model_objects.append(obj)

        return model_objects


