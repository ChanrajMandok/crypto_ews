import os

from token_risk_view_app.decorators import logger


def base_trading_urls(function=None, env_variable=None):
    """
    Decorator that injects the CoinMarketCap API's base URL.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            coinmarketcap_base_url = os.environ.get('COINMARKETCAP_BASE_URL', None)
            if not coinmarketcap_base_url:
                logger.warning("Environment variable 'COINMARKETCAP_BASE_URL' not set.")

            kwargs["coinmarketcap_base_url"] = coinmarketcap_base_url
   

            coinmarketcap_ccy_url = os.environ.get('COINMARKETCAP_CCY_URL', None)
            if not coinmarketcap_ccy_url:
                logger.warning("Environment variable 'COINMARKETCAP_CCY_URL' not set.")
            
            kwargs["coinmarketcap_ccy_url"] = coinmarketcap_ccy_url
            
            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator
