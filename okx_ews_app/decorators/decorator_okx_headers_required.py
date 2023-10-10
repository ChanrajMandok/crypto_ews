

def okx_headers_required(function=None, env_variable=None):
    """
    Decorator for views that checks that the user is logged in.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["okx_headers"] = {
                "authority": "www.okx.com",
                "method": "GET",
                "path": "/v2/support/home/web?t=1693901512770",
                "scheme": "https",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "App-Type": "web",
                "Referer": "https://www.okx.com/help-center/category/announcements",
                "Sec-Ch-Ua": ('"Chromium";v="116", "Not)A;Brand";v="24", '
                              '"Microsoft Edge";v="116"'),
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sentry-Trace": "b1bad08ef4a34d958c46b3e5d1d1b576-b94a039999fa53c7-1",
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"),
                "X-Cdn": "https://static.okx.com",
                "X-Locale": "en_US",
                "X-Utc": "1",
                "X-Zkdex-Env": "0"
            }
            return func(*args, **kwargs)
        return wrapper
    if function:
        return decorator(function)
    return decorator