import re
import requests

from bs4 import BeautifulSoup
from singleton_decorator import singleton

from defi_llama_ews_app.services import logger
from defi_llama_ews_app.decorator.decorator_defi_llama_urls_required import \
                                                     defi_llama_urls_required
from defi_llama_ews_app.decorator.decorator_defi_llama_json_headers_required import \
                                                     defi_llama_json_headers_required


@singleton
class ServiceDefiLamaUrlRetriever:

    @defi_llama_urls_required
    @defi_llama_json_headers_required
    def __init__(self,
                defi_lama_base_url,
                defi_lama_json_headers,
                **kwargs) -> None:
        self.base_url = defi_lama_base_url
        self.logger_instance = logger
        self.class_name = self.__class__.__name__
        self.url_headers = defi_lama_json_headers

    def get_hash_from_main_page(self, session):
        # Get the HTML content of the main page
        response = session.get(
                               url=self.base_url,
                               headers=self.url_headers)

        # Check status code
        if response.status_code - (response.status_code % 100) != 200:
            self.logger_instance.error(f"{self.class_name} {response.status_code}\
                             - ERROR: Failed to get a response from base URL: {self.base_url}")
            return None

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Search for hash in script tags
        for script in soup.find_all('script', attrs={"defer": ""}):
            src_content = script['src']
            if "/_next/static/" in src_content and "/chunks/" not in src_content:
                match = re.search(r"/_next/static/([a-zA-Z0-9]+)", src_content)
                if match:
                    return match.group(1)

        return None

    def retrieve(self, endpoint):
        max_tries = 3
        session = requests.Session()

        for _ in range(max_tries):
            try:
                # Retrieve the hash code
                hash_code = self.get_hash_from_main_page(session)
                
                # If hash code isn't found, log the error and retry
                if not hash_code:
                    self.logger_instance.error(f"{self.class_name}\
                                                - ERROR: Hash code not found.")
                    continue
                
                # Construct the full URL
                endpoint_url = f"{self.base_url}/_next/data/{hash_code}/{endpoint}"
                if endpoint_url:
                    return endpoint_url
                else:
                    return None

            except Exception as e:
                self.logger_instance.error(f"{self.class_name} - ERROR: {str(e)}")
                continue

        self.logger_instance.error(f"{self.class_name}\
                                    - ERROR: Max retries reached. Exiting...")
        return None