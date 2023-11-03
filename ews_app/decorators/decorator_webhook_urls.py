import os

from ews_app.decorators import logger


def webhooks_urls_required(function=None, env_variable=None):
    """
    Decorator that injects the webhook URLs.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cex_webhook = os.environ.get('CEX_WEBHOOK', None)
            if not cex_webhook:
                logger.warning("Environment variable 'CEX_WEBHOOK' not set.")
            kwargs["cex_webhook"] = cex_webhook

            defi_webhook = os.environ.get('DEFI_WEBHOOK', None)
            if not defi_webhook:
                logger.warning("Environment variable 'DEFI_WEBHOOK' not set.")
            kwargs["defi_webhook"] = defi_webhook

            stablecoin_webhook = os.environ.get('STABLECOIN_WEBHOOK', None)
            if not stablecoin_webhook:
                logger.warning("Environment variable 'STABLECOIN_WEBHOOK' not set.")
            kwargs["stablecoin_webhook"] = stablecoin_webhook

            token_webhook = os.environ.get('TOKEN_VOLATILITY_WEBHOOK', None)
            if not token_webhook:
                logger.warning("Environment variable 'TOKEN_VOLATILITY_WEBHOOK' not set.")
            kwargs["token_webhook"] = token_webhook

            pte_webhook = os.environ.get('PTE_VOLATILITY_WEBHOOK', None)
            if not pte_webhook:
                logger.warning("Environment variable 'PTE_VOLATILITY_WEBHOOK' not set.")
            kwargs["pte_webhook"] = pte_webhook

            token_liquidity_webhook = os.environ.get('TOKEN_LIQUIDITY_WEBHOOK_URL', None)
            if not token_liquidity_webhook:
                logger.warning("Environment variable 'TOKEN_LIQUIDITY_WEBHOOK_URL' not set.")
            kwargs["token_liquidity_webhook"] = token_liquidity_webhook

            return func(*args, **kwargs)
        
        return wrapper

    if function:
        return decorator(function)

    return decorator