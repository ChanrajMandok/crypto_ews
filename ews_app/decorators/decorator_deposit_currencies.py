import os

from ews_app.decorators import logger


def deposit_currencies_required(function=None, env_variable=None):
    """
    Decorator that injects the Deposit spot tickers list from the environment and formats it.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            ccy_namee_json = os.environ.get('CURRENCY_NAMES', None)
            
            if not ccy_namee_json:
                logger.warning("Environment variable 'CURRENCY_NAMES' not set.")
                return func(*args, **kwargs) 
            
            # Deserialize the JSON strings
            kwargs["ccy_namee_dict"] = { key: value for key, value in (x.split(':') for x in ccy_namee_json.split(','))}

            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator