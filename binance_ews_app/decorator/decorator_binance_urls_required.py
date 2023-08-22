import os

def binance_article_url_required(function=None, env_variable=None):
    """
    Decorator that injects the okx api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["binance_article_base_url"] = os.environ.get('BINANCE_ARTICLE_BASE_URL', None)
            kwargs["binance_news_list_url"] = os.environ.get('BINANCE_NEWS_LIST_URL', None)
            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator