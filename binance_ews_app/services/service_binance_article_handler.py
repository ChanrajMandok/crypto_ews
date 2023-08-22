import re
import datetime
from bs4 import BeautifulSoup

from binance_ews_app.services import logger


class ServiceBinanceArticleHandler:
    
    """
    Services extracts important Dates & article from HTML format 
    """
    
    def __init__(self):
        self.date_time_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*\(UTC\)")
        self.date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})(?!\s\d{2}:\d{2})")
    
    def handle(self, article_html_content: str, title: str) -> dict:
        try:
            article_content_text = self.extract_article_content(article_html_content, title)
            important_dates = self.extract_important_dates(article_content_text)
            
            return {
                'important_dates': important_dates,
                'article': article_content_text,
                'pop': len(important_dates) == 0  # True if no important dates are found
            }
        except Exception as e:
            logger.error(f"{self.__class__.__name__} - Unexpected error: {str(e)} for title: {title}")
            return {
                'important_dates': [],
                'article': '',
                'pop': True
            }

    def extract_article_content(self, article_html_content: str, title: str) -> str:
        soup = BeautifulSoup(article_html_content, 'html.parser')
        target_div = soup.find("div", {"id": "support_article"})

        if target_div:
            return target_div.get_text().strip()
        else:
            logger.warning(f"{self.__class__.__name__} - WARNING: Could not find target div for URL {title}")
            return ''

    def extract_important_dates(self, content: str) -> list:
        today = datetime.datetime.today()
        
        matches_date_time = self.date_time_pattern.findall(content)
        matches_date = self.date_pattern.findall(content)

        important_dates = []
        for match in matches_date_time:
            try:
                date_obj = datetime.datetime.strptime(match, "%Y-%m-%d %H:%M")
                if date_obj > today:
                    important_dates.append(match)
            except ValueError:
                logger.warning(f"{self.__class__.__name__} - WARNING: Invalid date-time format: {match}")

        for match in matches_date:
            try:
                date_obj = datetime.datetime.strptime(match, "%Y-%m-%d").date()
                if date_obj > today.date():
                    important_dates.append(match)
            except ValueError:
                logger.warning(f"{self.__class__.__name__} - WARNING: Invalid date format: {match}")

        return important_dates