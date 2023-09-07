import requests

class test():

    def test(self):
        response = requests.get('https://api.coinmarketcap.com/data-api/v3/chain/listing?limit=400')
        
        if response.status_code != 200:
            print(f"Failed to fetch data. HTTP status code: {response.status_code}")
            return []
        
        data = response.json()
        chain_list = data.get('data', {}).get('chainListingList', [])
        
        names = [chain['name'] for chain in chain_list]
        
        return names