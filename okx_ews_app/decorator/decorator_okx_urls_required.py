import os

def okx_url_required(function=None,
                                 env_variable=None):
    """
    Decorator that injects the okx api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["okx_article_base_url"] = \
                os.environ.get('OKX_ARTICLE_BASE_URL', None)
            kwargs["okx_news_dict_url"] = \
                os.environ.get('OKX_NEWS_DICT_URL', None)
            kwargs["okx_delist_url"] = \
                os.environ.get('OKX_DELIST_URL', None)
            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator