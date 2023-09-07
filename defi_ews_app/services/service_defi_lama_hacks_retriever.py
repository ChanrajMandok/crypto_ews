from defi_ews_app.services import logger
from defi_ews_app.services.service_defi_lama_html_retriever_interface \
                            import ServiceDefiLamaHtmlRetrieverInterface
from defi_ews_app.decorator.decorator_defi_lama_urls_required import \
                                                 defi_lama_url_required
from defi_ews_app.decorator.decorator_defi_lama_headers_required import \
                                                defi_lama_headers_required


class ServiceDefiLamaHacksRetriever(ServiceDefiLamaHtmlRetrieverInterface):

    @defi_lama_url_required
    @defi_lama_headers_required
    def __init__(self,
                 defi_lama_headers,
                 defi_lama_hacks_url) -> None:
        super().__init__()
        self._logger_instance  = logger
        self._headers          = defi_lama_headers
        self._url              = defi_lama_hacks_url
        self._table_selector   = "body > div:nth-child(1) > div > main > div:nth-child(3) > table > tbody"

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
            return final_data

        except Exception as e:
            self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
    

    
    
    
