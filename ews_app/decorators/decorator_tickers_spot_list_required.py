import os

from ews_app.decorators import logger


def spot_tickers_list_required(function=None, env_variable=None):
    """
    Decorator that injects the spot tickers list from the environment and formats it.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            raw_tickers_list = os.environ.get('SPOT_CURRENCIES', None)
            
            if not raw_tickers_list:
                logger.warning("Environment variable 'SPOT_CURRENCIES' not set.")
                return func(*args, **kwargs)  # Consider if you want to exit here or provide default behavior.
            
            raw_tickers_list = raw_tickers_list.split(" ")
            tickers_list = [t.replace("/", "") for t in raw_tickers_list]
            okx_tickers_list = [t.replace("/", "-") for t in raw_tickers_list]
            
            kwargs["tickers_spot_list_binance_format"] = tickers_list
            kwargs["raw_tickers_spot_list"] = raw_tickers_list
            kwargs["tickers_spot_list_okx_format"] = okx_tickers_list
            
            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator