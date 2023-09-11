from defi_ews_app.services import logger
from defi_ews_app.store.stores_defi import StoreDefi
from defi_ews_app.decorator.decorator_defi_lama_urls_required import \
                                                 defi_lama_url_required
from defi_ews_app.decorator.decorator_defi_lama_headers_required import \
                                               defi_lama_headers_required
from defi_ews_app.converters.converter_defi_lama_list_to_model_hack \
                               import ConverterDefiLamaListToModelHack
from defi_ews_app.service_interfaces.service_defi_html_retriever_interface \
                                    import ServiceDefiHtmlRetrieverInterface


class ServiceDefiLamaModelHackRetriever(ServiceDefiHtmlRetrieverInterface):

    @defi_lama_url_required
    @defi_lama_headers_required
    def __init__(self,
                 defi_lama_headers,
                 defi_lama_hacks_url) -> None:
        super().__init__()
        self._logger_instance            = logger
        self._headers                    = defi_lama_headers
        self._url                        = defi_lama_hacks_url
        self._converter                  = ConverterDefiLamaListToModelHack()
        self._store_db_defi_last_updated = StoreDefi.store_db_defi_last_updated
        self._table_selector             = "body > div:nth-child(1) > div > main > div:nth-child(3) > table > tbody"

    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def url(self):
        return self._url
    
    @property
    def url_headers(self):
        return self._headers
    
    @property
    def table_selector(self):
        return self._table_selector
    
    def retrieve(self):
        try:
            table_body = super().retrieve()
            rows = table_body.find_all("tr")

            def extract_data(cell):
                texts = list(cell.stripped_strings)
                hrefs = [a['href'] for a in cell.find_all("a", href=True)]
                return '; '.join(texts + hrefs)

            final_data = [[extract_data(cell) for cell in row.find_all(["td", "th"])] for row in rows]
            
            self._store_db_defi_last_updated.get()
            model_instances = []
            for value in final_data:
                if len(value) > 2: 
                    model_instances.append(self._converter.convert(value))
            
            return model_instances

        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")