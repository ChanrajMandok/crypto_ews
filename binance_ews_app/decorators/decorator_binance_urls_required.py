import os

from binance_ews_app.decorators import logger


def binance_url_required(function=None, env_variable=None):
    """
    Decorator that injects the binance api's base urls.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            binance_article_base_url = os.environ.get('BINANCE_ARTICLE_BASE_URL', None)
            if not binance_article_base_url:
                logger.error("Environment variable 'BINANCE_ARTICLE_BASE_URL' is not set.")
            kwargs["binance_article_base_url"] = binance_article_base_url

            binance_news_dict_url = os.environ.get('BINANCE_NEWS_DICT_URL', None)
            if not binance_news_dict_url:
                logger.error("Environment variable 'BINANCE_NEWS_DICT_URL' is not set.")
            kwargs["binance_news_dict_url"] = binance_news_dict_url

            binance_delist_url = os.environ.get('BINANCE_DELIST_URL', None)
            if not binance_delist_url:
                logger.error("Environment variable 'BINANCE_DELIST_URL' is not set.")
            kwargs["binance_delist_url"] = binance_delist_url

            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator