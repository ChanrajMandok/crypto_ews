import os


def wirex_spot_tickers_list(function=None, env_variable=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            raw_tickers_list = os.environ["SPOT_CURRENCIES"]
            raw_tickers_list = raw_tickers_list.split(" ")
            tickers_list = [t.replace("/", "") for t in raw_tickers_list]
            okx_tickers_list = [t.replace("/", "-") for t in raw_tickers_list]
            kwargs["wx_tickers_spot_list_binance_format"] = tickers_list
            kwargs["raw_tickers_spot_list"] = raw_tickers_list
            kwargs["wx_tickers_spot_list_okx_format"] = okx_tickers_list
            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator