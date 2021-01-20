import concurrent.futures as cf
import datetime
import math
import time
from typing import Optional, Tuple

import dateutil.parser
import requests
from peewee import IntegrityError
from web3 import Web3

from dfo.config import (AVG_BLOCK_TIME_HEURISTIC, DEBUG,
                        GRAPH_TOKEN_GROUP_SIZE, INFURA_ENDPOINT, INTERVAL,
                        ORCA_API_TOKEN, ORCA_API_URL, REQUEST_TIMEOUT,
                        UNISWAPV2_GRAPH_API_URL, UNISWAPV2_TOKENIDS,
                        timed_when_debug)
from dfo.db import APR, Price, prepared_db

database = prepared_db()


def get_dict_key_from_value(d: dict, v: float) -> str:
    return list(d.keys())[list(d.values()).index(v)]


# one APR measurement looks like
# "AaveLend":{"ABAT":1006749739214744,"ABUSD":115850335586733570,"ADAI":45113613081041280,"AENJ":63300177299645,"AETH":796278847645440,"AKNC":363087816857036, [...],"Platform":"Aave","_measurement":"Lend","_start":"2019-12-30T09:43:15.496889159Z","_stop":"2020-12-29T15:43:15.496889159Z","result":"_result","table":0}

@timed_when_debug
def get_apr() -> None:
    """polling data from the orcadefi API"""
    query = f"{ORCA_API_URL}all?token={ORCA_API_TOKEN}"
    try:
        response = requests.get(url=query, timeout=REQUEST_TIMEOUT)
        with database:
            for measurement in response.json().values():
                side = measurement['_measurement']
                if side != 'Lend': continue # we assume we won't swap on the Borrow side
                platform = measurement['Platform']
                # start = measurement['_start']
                stop = measurement['_stop'] # FIXME strange intervals. here we're using just using stop as datetime
                for k in measurement.keys():
                    if k.isupper():
                        token = k
                        utctime = dateutil.parser.isoparse(stop)
                        try:
                            APR.create(
                                platform = platform,
                                datetime = utctime,
                                token = token,
                                value = measurement[token],
                            )
                        except IntegrityError as e:
                            print(f'poll_apr: ({platform=} {utctime=} {token=}) - {e}')
    except requests.Timeout:
        print(f'poll_apr: timeout')
    except requests.exceptions.ConnectionError:
        print(f'poll_apr: connection error')


def datetimeutc_from_block_heuristic(blocknumber: int) -> datetime.datetime:
    #FIXME this heuristic is not good
    print('using heuristic for block time')
    approx_seconds_since_genesis =  datetime.timedelta(seconds=(blocknumber * AVG_BLOCK_TIME_HEURISTIC))
    genesis_datetime = datetime.datetime(2015, 7, 30, 15, 26, 28, tzinfo=datetime.timezone.utc)
    return approx_seconds_since_genesis + genesis_datetime


def datetimeutc_from_block(blocknumber: int) -> Tuple[datetime.datetime, str]:
    # if web3 request fails, use heuristic
    try:
        w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))
        block = w3.eth.getBlock('latest')
        return (datetime.datetime.fromtimestamp(block.timestamp, tz=datetime.timezone.utc), 'web3')
    except requests.Timeout:
        return (datetimeutc_from_block_heuristic(blocknumber), 'heuristic')


@timed_when_debug
def graph_query(url: str, query: str) -> Optional[dict]:
    try:
        response = requests.post(url, timeout=REQUEST_TIMEOUT, json={'query': query})
        try:
            return response.json()['data']
        except KeyError:
            print(f'graph_query: failed with the following error(s):')
            for error in response.json()['errors']:
                print(error['message'])
            return None
    except Exception as e:
        print(f'graph_query ({url}) Exception: {e}')


# one price measurement looks like:
# {"data":{"_meta":{"block":{"number":11628472}},"bundle":{"ethPrice":"1275.37112457166793163706177720231","id":"1"},"tokens":[{"derivedETH":"26.49797471454524981810278279931884","id":"0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e"},{"derivedETH":"30.10764138025488740785364887131035","id":"0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"}, [...]

def get_price() -> None:
    """
    polling data from the uniswapv2 subgraph
    we do multiple queries because a single big query results in processing errors on thegraph.com
    if one query fails in the sequence, we fail the sequence and don't commit to database
    """
    try:
        # 'meta' query
        eth_price_query = 'bundle(id: 1) { id ethPrice }'
        block_info_query = '_meta { block { number } }'
        query_meta  = '{ %s %s }' % (block_info_query, eth_price_query)
        data_meta = graph_query(UNISWAPV2_GRAPH_API_URL, query_meta)
        if data_meta == None:
            print(f'query failed: {query_meta}')
            return None
        ethprice = float(data_meta['bundle']['ethPrice'])
        blocknumber = data_meta['_meta']['block']['number']
        datetimeutc, timesource = datetimeutc_from_block(blocknumber)

        # obtain prices in a few queries
        tokensids = list(UNISWAPV2_TOKENIDS.values())
        partitions = math.floor(len(tokensids) / GRAPH_TOKEN_GROUP_SIZE) + 1
        lists_tokenids = [
            tokensids[GRAPH_TOKEN_GROUP_SIZE*i : GRAPH_TOKEN_GROUP_SIZE*(i+1)]
            for i in range(partitions)
        ]
        token_prices = {}
        for group in lists_tokenids:
            list_tokenids_str = ','.join([f'"{tokenid}"' for tokenid in group])
            query = '{ tokens (where: {id_in: [ %s ]}) { id derivedETH } }' % list_tokenids_str
            token_data = graph_query(UNISWAPV2_GRAPH_API_URL, query)
            if token_data == None:
                print(f'query failed: {query}')
                return None
            for token in token_data['tokens']:
                token_prices[token['id']] = ethprice * float(token['derivedETH'])

        with database:
            for token in token_prices:
                value = token_prices[token]
                tokenid = get_dict_key_from_value(UNISWAPV2_TOKENIDS, token)
                try:
                    Price.create(datetime=datetimeutc, token=tokenid, value=value, source=timesource)
                except IntegrityError as e:
                    print(f'poll_price: ({datetimeutc=} {tokenid=} {value=} {timesource=}) - {e}')
            
    except requests.Timeout:
        print(f'poll_price: timeout')
    except requests.exceptions.ConnectionError:
        print(f'poll_price: connection error')


def run() -> None:
    datagetters = [
        get_apr,
        get_price
    ]
    with cf.ThreadPoolExecutor(max_workers=len(datagetters)) as pool:
        while True:
            t_start = time.time()
            # each future has the responsibility to end
            fs = [pool.submit(f) for f in datagetters]
            [f.result() for f in cf.as_completed(fs)]
            duration = time.time() - t_start
            print(f'{datetime.datetime.now()}: collection round done in {duration:.2f} seconds')
            time.sleep(INTERVAL - duration)
