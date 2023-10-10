import os

from ews_app.decorators import logger


def decorator_refresh_increments(function=None, env_variable=None):
    """
    Decorator that provides various refresh increments.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager_increment = os.environ.get('MANAGER_REFRESH_INCREMENT_MINS', None)
            if not manager_increment:
                logger.warning("Environment variable 'MANAGER_REFRESH_INCREMENT_MINS' not set")
                manager_increment = 10
            kwargs["manager_refresh_increment_mins"] = int(manager_increment)

            update_increment = os.environ.get('UPDATE_REFRESH_INCREMENT_MINS', None)
            if not update_increment:
                logger.warning("Environment variable 'UPDATE_REFRESH_INCREMENT_MINS' not set")
                update_increment = 10
            kwargs["update_refresh_increment_mins"] = int(update_increment)

            defi_llama_increment = os.environ.get('DEFI_LLAMA_UPDATE_REFRESH_INCREMENT_MINS', None)
            if not defi_llama_increment:
                logger.warning("Environment variable 'DEFI_LLAMA_UPDATE_REFRESH_INCREMENT_MINS' not set")
                defi_llama_increment = 10
            kwargs["defi_llama_refresh_increment_mins"] = int(defi_llama_increment)

            orderbooks_increment = os.environ.get('ORDERBOOKS_REFRESH_INCREMENT_MINS', None)
            if not orderbooks_increment:
                logger.warning("Environment variable 'ORDERBOOKS_REFRESH_INCREMENT_MINS' not set")
                orderbooks_increment = 1
            kwargs["orderbooks_refresh_increment_mins"] = int(orderbooks_increment)

            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator