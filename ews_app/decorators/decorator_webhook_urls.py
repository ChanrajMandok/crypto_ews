import os


def webhooks_urls_required(function=None, env_variable=None):
    """
    Decorator that injects the okx api's base url.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["cex_webhook"] = \
                os.environ.get('CEX_WEBHOOK', None)        
            kwargs["defi_webhook"] = \
                os.environ.get('DEFI_WEBHOOK', None)
            kwargs["stablecoin_webhook"] = \
                os.environ.get('STABELCOIN_WEBHOOK', None)
            kwargs["token_webhook"] = \
                os.environ.get('TOKEN_VOLATILITY_WEBHOOK', None)
            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator