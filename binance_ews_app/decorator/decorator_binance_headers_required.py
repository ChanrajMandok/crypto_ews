def binance_headers_required(function=None, env_variable=None):
    """
    Decorator for views that checks that the user is logged in.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["binance_headers"] = {
                                "authority": "www.binance.com",
                                "method": "GET",
                                "path": "/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=20&pageNo=1",
                                "scheme": "https",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "Accept-Encoding": "gzip, deflate, br",
                                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
                                "Cache-Control": "max-age=0",
                                "Cp-Extension-Installed": "Yes",
                                "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
                                "Sec-Ch-Ua-Mobile": "?0",
                                "Sec-Ch-Ua-Platform": "Windows",
                                "Sec-Fetch-Dest": "document",
                                "Sec-Fetch-Mode": "navigate",
                                "Sec-Fetch-Site": "none",
                                "Sec-Fetch-User": "?1",
                                "Upgrade-Insecure-Requests": "1",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
                            }

            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator