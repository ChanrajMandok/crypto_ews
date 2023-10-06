import os


def orderbooks_urls_required(function=None, env_variable=None):
    """
    Decorator that injects the okx api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = env_variable or 'OKX_ORDERBOOK_URL'
            kwargs["okx_orderbooks_url"] = os.environ[key]
            key = env_variable or 'BINANCE_ORDERBOOK_URL'
            kwargs["binance_orderbooks_url"] = os.environ[key]
            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator