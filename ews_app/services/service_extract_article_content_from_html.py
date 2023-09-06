from bs4 import BeautifulSoup

from ews_app.services import logger
from ews_app.enum.enum_source import EnumSource


class ServiceExtractArticleContentFromHtml:
     
    def extract_article_content(self, 
                                source: EnumSource.choices(),
                                article_html_content: str) -> str:
            

            soup = BeautifulSoup(article_html_content, 'html.parser')

            if source == EnumSource.BINANCE:
                target_div = soup.find("div", {"id": "support_article"})
            
            if source == EnumSource.OKX:
                target_div = soup.find("div", {"class": "article-main-content"})

            if not target_div:
                logger.error(f"{self.__class__.__name__} - Unable to find target div in HTML content")
                return ''    

            # Replace <li> elements with the text followed by a unique separator
            for li in target_div.find_all("li"):
                li.string = li.get_text() + " "
                
            content_with_separators = target_div.get_text().strip()
            
            return content_with_separators