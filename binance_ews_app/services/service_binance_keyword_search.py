import os
from datetime import datetime

from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords


class ServiceBinanceKeywordSearch:
    
    """
    Services Searches Titles of News Dict (Catalogs) for Keywords and ensures the Events are 
    within lookwback window of 30 days 
    """

    def __init__(self) -> None:
        self.lookback_days = int(os.environ.get('RELEVENT_NEWS_LOOKBACK_DAYS', int(30)))

    def search_catalogs(self, catalogs: list[dict]) -> list[dict]:
        
        relevent_articles = []
        current_ts = int(datetime.utcnow().timestamp() * 1000)
        keywords = {keyword.name.lower() for keyword in EnumHighAlertWarningKeyWords}
        
        for catalog in catalogs:
            
            if not isinstance(catalog, dict):
                continue
            
            articles = catalog.get('articles', [])
            if not isinstance(articles, list):
                continue
            
            for article in articles:
                if not isinstance(article, dict):
                    continue

                date = article.get('releaseDate', '')
                
                try:
                    release_ts = int(date) if date else 0
                except ValueError:
                    continue
                
                if not (current_ts - release_ts <= self.lookback_days * 24 * 60 * 60 * 1000):
                    continue

                title = article.get('title', '')

                if not isinstance(title, str):
                    continue

                title = title.lower()

                for keyword_enum in keywords:
                    if keyword_enum in title:
                        article_copy = article.copy()  # Create a shallow copy to avoid modifying the original
                        article_copy['Alert_Category'] = EnumHighAlertWarningKeyWords(keyword_enum).name
                        relevent_articles.append(article_copy)
                        break  

        return relevent_articles

        

     