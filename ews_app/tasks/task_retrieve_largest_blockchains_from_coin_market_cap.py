import requests


class TaskRetrieveLargestBlockchainsFromCoinMarketCap():

    def run(self):
        response = requests.get('https://api.coinmarketcap.com/data-api/v3/chain/listing?limit=100')
        
        if response.status_code != 200:
            print(f"Failed to fetch data. HTTP status code: {response.status_code}")
            return []
        
        data = response.json()
        chain_list = data.get('data', {}).get('chainListingList', [])
        
        formatted_list = [f"{chain['name'].upper()} = {chain['nativeToken'] if 'nativeToken' in chain else 'nan'}" for chain in chain_list]

        return formatted_list