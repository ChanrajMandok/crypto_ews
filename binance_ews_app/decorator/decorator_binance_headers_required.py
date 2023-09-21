
def binance_headers_required(function=None, 
                             env_variable=None):
    """
    Decorator for views that checks that the user is logged in.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["binance_headers"] = {
                "authority": "www.binance.com",
                "method": "GET",
                "path": ("/bapi/composite/v1/public/cms/article/list/query?"
                         "type=1&pageSize=20&pageNo=1"),
                "scheme": "https",
                "Accept": ("text/html,application/xhtml+xml,application/xml;"
                           "q=0.9,image/webp,image/apng,*/*;q=0.8,"
                           "application/signed-exchange;v=b3;q=0.7"),
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
                "Cache-Control": "max-age=0",
                "Cp-Extension-Installed": "Yes",
                "Sec-Ch-Ua": ('"Not/A)Brand";v="99", "Microsoft Edge";v="115",'
                              ' "Chromium";v="115"'),
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203")
                                         }
            kwargs["binance_delist_headers"] = {
                    'authority': 'www.binance.com',
                    'method': 'GET',
                    'path': '/bapi/asset/v2/public/asset-service/product/get-products'
                            '?includeEtf=true',
                    'scheme': 'https',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Bnc-Location': 'BINANCE',
                    'Bnc-Uuid': '4f35901a-a464-471a-a473-e87c3083349e',
                    'Clienttype': 'web',
                    'Content-Type': 'application/json',
                    'Csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
                    'Device-Info': '{"screener_resolution": "2560x1440", "affiliate_screener_resolution": "2560x1440", '
                                '"system_version": "Windows 10", "browser_mode": "unkown", "system_lang": "en-US", '
                                '"timezone_offset": -60, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31", '
                                '"device_name": "Edge V117.0.2045.31 (Windows)", "platform": "Windows"}',
                    'Fvideo-Id': '33c56a9ecc7caef89baf89054ec69f06ccbc5bff',
                    'Lang': 'en',
                    'Referer': 'https://www.binance.com/en/trade/ASR_BUSD?theme=dark&type=spot',
                    'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                    'Sec-Ch-Ua-Mobile': '?0',
                    'Sec-Ch-Ua-Platform': '"Windows"',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
                    'X-Passthrough-Token': '',
                    'X-Trace-Id': 'fac0a000-34df-442d-b3b1-89229c67f12c',
                    'X-Ui-Request-Trace': 'fac0a000-34df-442d-b3b1-89229c67f12c'
                                                }




            return func(*args, **kwargs)
        return wrapper

    if function:
        return decorator(function)

    return decorator