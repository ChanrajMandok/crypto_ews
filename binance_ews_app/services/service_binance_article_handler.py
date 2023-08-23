import re
import datetime
from bs4 import BeautifulSoup

from binance_ews_app.services import logger


class ServiceBinanceArticleHandler:
    """
    Service extracts important Dates, articles, trading pairs, 
    and specific contract trading pairs from HTML format.
    """

    def __init__(self):
        self.pairs_pattern = re.compile(r"([A-Z0-9]{3,10})\/([A-Z0-9]{3,10})")
        self.date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?)")
        self.contract_pairs_pattern = re.compile(r"USDⓈ-M ((?:[A-Z0-9]{1,10}[A-Z0-9]{1,10}(?: and )?)+) Perpetual Contract")

    def handle(self, article_html_content: str, title: str, url: str) -> dict:
        try:
            article_content_text = self.extract_article_content(article_html_content)
            important_dates = self.extract_important_dates(article_content_text)
            trading_pairs = self.extract_trading_pairs(article_content_text)
            contract_pairs = self.extract_contract_pairs(article_content_text)

            return {
                'url': url,
                'important_dates': important_dates,
                'article': article_content_text,
                'pop': not important_dates,
                'spot_pairs': trading_pairs,
                'USDⓈ-M_pairs': contract_pairs
            }
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - Unexpected error: {str(e)} for title: {title}")
            return {
                'url': url,
                'important_dates': [],
                'article': '',
                'pop': True,
                'trading_pairs': [],
                'contract_pairs': []
            }

    def extract_article_content(self, article_html_content: str) -> str:
        soup = BeautifulSoup(article_html_content, 'html.parser')
        target_div = soup.find("div", {"id": "support_article"})
        return target_div.get_text().strip() if target_div else ''

    def extract_important_dates(self, content: str) -> list:
        today = datetime.datetime.today()
        
        important_dates = []
        for match in self.date_pattern.findall(content):
            if ' ' in match:  # Check if time is included
                date_format = "%Y-%m-%d %H:%M"
            else:
                date_format = "%Y-%m-%d"

            date_obj = datetime.datetime.strptime(match, date_format)
            if date_obj > today:
                important_dates.append(match)

        return important_dates

    def extract_trading_pairs(self, content: str) -> list:
        return [f"{match[0]}/{match[1]}" for match in self.pairs_pattern.findall(content)]

    def extract_contract_pairs(self, content: str) -> list:
        matches = self.contract_pairs_pattern.findall(content)
        return [pair for match in matches for pair in match.split(" and ")]