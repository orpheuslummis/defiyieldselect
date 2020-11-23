import requests

def get_yieldfi_rate(protocol, asset):
    return requests.get(f"https://api.yield.fi/lending/rate?protocol={protocol}&asset={asset}").json()
