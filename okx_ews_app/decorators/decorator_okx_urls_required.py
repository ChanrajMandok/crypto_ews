import os

from okx_ews_app.decorators import logger


def okx_url_required(function=None, env_variable=None):
    """
    Decorator that injects the OKX API's base URL.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            okx_article_base_url = os.environ.get('OKX_ARTICLE_BASE_URL', None)
            if not okx_article_base_url:
                logger.warning("Environment variable 'OKX_ARTICLE_BASE_URL' not set.")
            kwargs["okx_article_base_url"] = okx_article_base_url

            okx_news_dict_url = os.environ.get('OKX_NEWS_DICT_URL', None)
            if not okx_news_dict_url:
                logger.warning("Environment variable 'OKX_NEWS_DICT_URL' not set.")
            kwargs["okx_news_dict_url"] = okx_news_dict_url

            okx_delist_url = os.environ.get('OKX_DELIST_URL', None)
            if not okx_delist_url:
                logger.warning("Environment variable 'OKX_DELIST_URL' not set.")
            kwargs["okx_delist_url"] = okx_delist_url

            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator