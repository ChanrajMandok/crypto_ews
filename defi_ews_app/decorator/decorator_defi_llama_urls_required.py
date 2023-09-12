import os

def defi_llama_url_required(function=None,
                                 env_variable=None):
    """
    Decorator that injects the defi lama api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["defi_lama_hacks_url"] = \
                os.environ.get('DEFI_HACKS_URL', None)
            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator