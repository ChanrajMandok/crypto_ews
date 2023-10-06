import os


def decorator_refresh_increments(function=None, env_variable=None):
    """
    Decorator that injects the okx api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["manager_refresh_increment_mins"] = \
                int(os.environ.get('MANAGER_REFRESH_INCREMENT_MINS', 10))
            kwargs["update_refresh_increment_mins"] = \
                int(os.environ.get('UPDATE_REFRESH_INCREMENT_MINS', 10))
            kwargs["defi_llama_refresh_increment_mins"] = \
                int(os.environ.get('DEFI_LLAMA_UPDATE_REFRESH_INCREMENT_MINS', 10))
            kwargs["orderbooks_refresh_increment_mins"] = \
                int(os.environ.get('ORDERBOOKS_REFRESH_INCREMENT_MINS', 1))
                        
        return wrapper

    if function:
        return decorator(function)

    return decorator