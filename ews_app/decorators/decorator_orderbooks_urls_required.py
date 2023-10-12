import os

from ews_app.decorators import logger


def orderbooks_urls_required(function=None, env_variable=None):
    """
    Decorator that injects the okx and binance api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = env_variable or 'OKX_ORDERBOOK_URL'
            okx_orderbooks_url = os.environ.get(key, None)
            if not okx_orderbooks_url:
                logger.error(f"Environment variable '{key}' is not set.")
            kwargs["okx_orderbooks_url"] = okx_orderbooks_url

            key = env_variable or 'BINANCE_ORDERBOOK_URL'
            binance_orderbooks_url = os.environ.get(key, None)
            if not binance_orderbooks_url:
                logger.error(f"Environment variable '{key}' is not set.")
            kwargs["binance_orderbooks_url"] = binance_orderbooks_url

            key = env_variable or 'BASE_CURRENCIES'
            base_ccys_str = os.environ.get(key)
        
            if not base_ccys_str:
                logger.error(f"Environment variable '{key}' is not set.")
                base_ccys = []
            else:
                base_ccys = [ccy.strip() for ccy in base_ccys_str.split(",")]

            kwargs["base_ccys"] = base_ccys
            
            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator