import os

def base_trading_urls(function=None,
                                 env_variable=None):
    """
    Decorator that injects the okx api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["coinmarketcap_base_url"] = \
                os.environ.get('COINMARKETCAP_BASE_URL', None)
            return func(*args, **kwargs)
        
        
        return wrapper

    if function:
        return decorator(function)

    return decorator