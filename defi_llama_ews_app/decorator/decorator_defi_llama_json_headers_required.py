def defi_llama_json_headers_required(function=None, env_variable=None):
    """
    Decorator for views that checks that the user is logged in.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["defi_lama_json_headers"] = \
            {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "If-None-Match": 'W/"16pn4o3wb3ypkpj"',
                "Purpose": "prefetch",
                "Referer": "https://defillama.com/bridges",
                "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
                "X-Nextjs-Data": "1"
            }
            return func(*args, **kwargs)
        return wrapper
    if function:
        return decorator(function)
    return decorator
