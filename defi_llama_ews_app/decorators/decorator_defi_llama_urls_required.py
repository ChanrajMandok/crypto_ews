import os

from defi_llama_ews_app.decorators import logger


def defi_llama_urls_required(function=None, env_variable=None):
    """
    Decorator that injects the defi lama api's base urls.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            defi_llama_hacks_url = os.environ.get('DEFI_LLAMA_HACKS_URL', None)
            if not defi_llama_hacks_url:
                logger.error("Environment variable DEFI_LLAMA_HACKS_URL is not set.")
            kwargs["defi_llama_hacks_url"] = defi_llama_hacks_url

            defi_llama_base_url = os.environ.get('DEFI_LLAMA_BASE_URL', None)
            if not defi_llama_base_url:
                logger.error("Environment variable DEFI_LLAMA_BASE_URL is not set.")
            kwargs["defi_llama_base_url"] = defi_llama_base_url

            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator