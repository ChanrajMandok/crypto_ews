from binance_ews_app.services.service_binance_keyword_search import ServiceBinanceKeywordSearch
from binance_ews_app.services.service_binance_article_handler import ServiceBinanceArticleHandler
from binance_ews_app.services.service_binance_article_retriever import ServiceBinanceArticleRetriever
from binance_ews_app.services.service_binance_news_html_retriever import ServiceBinanceyNewsHtmlRetriever


class ServiceMain:
    
    def __init__(self) -> None:
        self.service_binance_keyword_search = ServiceBinanceKeywordSearch()
        self.service_binance_article_handler = ServiceBinanceArticleHandler()
        self.service_binance_article_retriever = ServiceBinanceArticleRetriever()
        self.service_binance_news_html_retriever = ServiceBinanceyNewsHtmlRetriever()
        
        
    def main(self):
        # retrieve all recent news articles & announcements from binance
        articles = self.service_binance_article_retriever.retrieve()
        # filter news articles & announcements for specific values
        key_articles_dict = self.service_binance_keyword_search.search_articles(articles=articles)
        # now pull articles from binance, via beautiful soup to pull relevent infomation
        dict_w_articles = self.service_binance_news_html_retriever.retrieve(key_articles_dict)
        # create store and when relevent updates occur create webhook which notifies relevent parties. 