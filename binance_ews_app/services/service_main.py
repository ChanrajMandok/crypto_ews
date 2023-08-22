from binance_ews_app.services.service_binance_keyword_search import ServiceBinanceKeywordSearch
from binance_ews_app.services.service_binance_news_dict_retriever import ServiceBinanceNewsDictRetriever
from binance_ews_app.services.service_binance_news_html_retriever import ServiceBinanceyNewsHtmlRetriever
from binance_ews_app.services.service_binance_article_handler import ServiceBinanceArticleHandler


class ServiceMain:
    
    def __init__(self) -> None:
        self.service_binance_keyword_search = ServiceBinanceKeywordSearch()
        self.service_binance_key_news_retriever = ServiceBinanceNewsDictRetriever()
        self.service_binance_article_handler = ServiceBinanceArticleHandler()
        self.service_binance_priority_news_retriever = ServiceBinanceyNewsHtmlRetriever()
        
    def main(self):
        # retrieve all recent news articles & announcements from binance
        catalouges = self.service_binance_key_news_retriever.retrieve()
        # filter news articles & announcements for specific values
        key_articles_dict = self.service_binance_keyword_search.search_catalogs(catalogs=catalouges)
        # now pull articles from binance, via beautiful soup to pull relevent infomation
        dict_w_articles = self.service_binance_priority_news_retriever.retrieve(key_articles_dict)
        # relevent articles are put into handlers