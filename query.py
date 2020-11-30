import requests

def get_historical_rates(protocol, asset):
    return get_yieldfi_rate(protocol, asset)

# NOTE this service might not stay available, and it doesn't give historical data since the beginning
def get_yieldfi_rate(protocol, asset):
    return requests.get(f"https://api.yield.fi/lending/rate?protocol={protocol}&asset={asset}").json()
