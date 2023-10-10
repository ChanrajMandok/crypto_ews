

def defi_llama_headers_required(function=None, env_variable=None):
    """
    Decorator for views that checks that the user is logged in.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["defi_llama_headers"] = {
                "authority": "defillama.com",
                "method": "GET",
                "path": "/hacks",
                "scheme": "https",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                        "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "max-age=0",
                "Referer": "https://www.bing.com/",
                "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", '
                            '"Microsoft Edge";v="116"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"
            }
            return func(*args, **kwargs)
        return wrapper
    if function:
        return decorator(function)
    return decorator