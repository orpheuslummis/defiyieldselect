# Configuring tokens:
# 1. APR_TOKEN_TO_UNISWAPV2_TOKENS is a mapping from APR token name to Uniswap token name.
#    The APR token will be read from the APR API's data
# 2. UNISWAPV2_TOKENIDS is a mapping from Uniswap token name to Uniswap token address for price data

# here, time units are seconds

import os

from web3.main import Web3

MODEL_MAIN = 'model_a'
MODEL_A_PRICE_WEIGHT = 2000.0

PAST_HORIZON = 1200.0

RESAMPLING_INTERVAL = '1min'

# interval for scoring and for data collection
INTERVAL = 60.0
REQUEST_TIMEOUT = 20.0  # graphql takes a while!
assert INTERVAL >= REQUEST_TIMEOUT * 2 # to ensure the thread pool behaves well

PORT = 8000
HOST = '0.0.0.0'

DATA_PATH = 'data'
os.makedirs(DATA_PATH, exist_ok=True)

ORCA_API_URL = 'http://orcadefi.com:10000/api/v1/realtime/'
ORCA_API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMyNDU2MSIsIm5hbWUiOiJNaXJvc2xhdiIsImlhdCI6Nzg5NDUyMTIzNTZ9.GQ5LR3jdhmTl_rmKgNPzrgNRrx9nflhJBiEgjz5Coec'
ORCA_API_MANTISSA = 1e18

# Endpoint access provided until March 2021
INFURA_ENDPOINT = 'https://mainnet.infura.io/v3/eb577b703a3e4db89f756b660db47f6c'

UNISWAPV2_GRAPH_API_URL = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
GRAPH_TOKEN_GROUP_SIZE = 8  # query in smaller group to avoid processing errors


UNISWAPV2_TOKENIDS = {
    'BAT': '0x0D8775F648430679A709E98d2b0Cb6250d2887EF',
    'BUSD': '0x4Fabb145d64652a948d72533023f6E7A623C7C53',
    'BZRX': '0x56d811088235F11C8920698a204A5010a788f4b3',
    'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    'ENJ': '0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c',
    'KNC': '0xdd974D5C2e2928deA5F71b9825b8b646686BD200',
    'LEND': '0x80fB784B7eD66730e8b1DBd9820aFD29931aab03',
    'LINK': '0x514910771AF9Ca656af840dff83E8264EcF986CA',
    'MANA': '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942',
    'MKR': '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2',
    'REN': '0x408e41876cCCDC0F92210600ef50372656052a38',
    'REP': '0x221657776846890989a759BA2973e427DfF5C9bB',
    'SAI': '0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359',
    'SNX': '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F',
    'SUSD': '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51',
    'TUSD': '0x0000000000085d4780B73119b644AE5ecd22b376',
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'WBTC': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
    'WETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
    'YFI': '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e',
    'ZRX': '0xE41d2489571d322189246DaFA5ebDe1F4699F498',
}
# the IDs are written in a checksum address format
for t in UNISWAPV2_TOKENIDS:
    assert Web3.isChecksumAddress(UNISWAPV2_TOKENIDS[t])
# but the uniswapv2 subgraph wants them lower case!
for t in UNISWAPV2_TOKENIDS:
    UNISWAPV2_TOKENIDS[t] = UNISWAPV2_TOKENIDS[t].lower()


APR_TOKEN_TO_UNISWAPV2_TOKENS = {
    'CZRX': 'ZRX',
    'ABUSD': 'BUSD',
    'CBAT': 'BAT',
    'AREP': 'REP',
    'DUSDC': 'USDC',
    'AUSDC': 'USDC',
    'AZRX': 'ZRX',
    'AKNC': 'KNC',
    'CETH': 'WETH',
    'AYFI': 'YFI',
    'AWBTC': 'WBTC',
    'ALEND': 'LEND',
    'IBZRX': 'BZRX',
    'AENJ': 'ENJ',
    'AUSDT': 'USDT',
    'DDAI': 'DAI',
    'IETH': 'WETH',
    'CDAI': 'DAI',
    'IDAI': 'DAI',
    'CUSDT': 'USDT',
    'AETH': 'WETH',
    'IMKR': 'MKR',
    'ABAT': 'BAT',
    'CSAI': 'SAI',
    'CUSDC': 'USDC',
    'AMANA': 'MANA',
    'ILINK': 'LINK',
    'ASUSD': 'SUSD',
    'ATUSD': 'TUSD',
    'ILEND': 'LEND',
    'ASNX': 'SNX',
    'IWBTC': 'WBTC',
    'IYFI': 'YFI',
    'ALINK': 'LINK',
    'IUSDC': 'USDC',
    'ADAI': 'DAI',
    'IKNC': 'KNC',
    'CREP': 'REP',
    'AMKR': 'MKR',
    'CWBTC': 'WBTC',
    'IUSDT': 'USDT',
    'AREN': 'REN',
    'DETH': 'WETH',
    'DSAI': 'SAI'
}
assert set(APR_TOKEN_TO_UNISWAPV2_TOKENS.values()) ==  set(UNISWAPV2_TOKENIDS.keys())
APR_TOKENS = APR_TOKEN_TO_UNISWAPV2_TOKENS.keys() # a shorthand


# heuristic for when Infura is not available:
# using recent block time to avoid querying the ethereum blockchain for datetime information of blocks
# ref: https://etherscan.io/chart/blocktime
# although the average block time from genesis is 14.49:
#   first ethereum block: Jul-30-2015 03:26:28 PM +UTC
#   recent block: 11675081 at Jan-17-2021 09:10:49 PM +UTC
#   timespan: datetime.timedelta(days=1998, seconds=20661)
#   11675081/(timespan.total_seconds) = 14.787722757555173
# FIXME currently the heuristic is quite erroneous
AVG_BLOCK_TIME_HEURISTIC = 13.0 # seconds


if os.getenv('DEBUG') == 'True':
    DEBUG = True
else:
    DEBUG = False