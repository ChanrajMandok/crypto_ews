import os
from datetime import datetime

from ews_app.enum.enum_priority import EnumPriority
from ews_app.enum.enum_false_altert_phrases import EnumFalseAlertPhrases
from ews_app.enum.enum_low_alert_warning_key_words import EnumLowAlertWarningKeyWords
from ews_app.enum.enum_high_alert_warning_key_words import EnumHighAlertWarningKeyWords


class ServiceBinanceKeywordSearch:
    """
    Services Searches Titles of News Dict (Catalogs) for Keywords and ensures the Events are 
    within lookback window of 30 days 
    """
    
    def __init__(self) -> None:
        self.lookback_days = int(os.environ.get('RELEVENT_NEWS_LOOKBACK_DAYS', 30))
        self.high_priority_keywords = {keyword.name.lower() for keyword in EnumHighAlertWarningKeyWords}
        self.low_priority_keywords = {keyword.name.lower() for keyword in EnumLowAlertWarningKeyWords}
        self.false_alert_phrases = {phrase.name.lower() for phrase in EnumFalseAlertPhrases}
        self.max_lookback_time = self.lookback_days * 24 * 60 * 60 * 1000

    def _contains_false_alert(self, title_words):
        return self.false_alert_phrases & title_words

    def search_catalogs(self, catalogs: list[dict]) -> list[dict]:
        
        relevant_articles = []
        current_ts = int(datetime.utcnow().timestamp() * 1000)
        
        for catalog in catalogs:
            if not isinstance(catalog, dict):
                continue

            articles = catalog.get('articles', [])
            if not articles:
                continue

            for article in articles:
                if not isinstance(article, dict):
                    continue
                
                title = article.get('title', '')
                if not isinstance(title, str):
                    continue
                
                title = title.lower()
                title_words = set(title.split())

                # False alert check
                if self._contains_false_alert(title_words):
                    continue

                # Time check
                release_ts = int(article.get('releaseDate', 0))
                if current_ts - release_ts > self.max_lookback_time:
                    continue

                # High priority check
                intersected_keywords = title_words & self.high_priority_keywords
                if intersected_keywords:
                    priority = EnumPriority.HIGH
                    keyword_found = list(intersected_keywords)[0]
                else:
                    intersected_keywords = title_words & self.low_priority_keywords
                    if intersected_keywords:
                        priority = EnumPriority.LOW
                        keyword_found = list(intersected_keywords)[0]
                    else:
                        continue

                article_copy = article.copy()
                article_copy['Alert_Category'] = keyword_found.upper()
                article_copy['Alert_Priority'] = priority
                relevant_articles.append(article_copy)

        return relevant_articles
