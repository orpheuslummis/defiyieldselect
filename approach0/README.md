# DeFi yield optimization

overview: get the timeseries of the interest rates, predict which will be the highest, move accordingly


## how are the interests collected in each protocol?

in Compound: 

in Aave: the balance in the contract will increase. Therefore at redemption, there will be a higher amount than what was initially deposited.


## data acquisition

csv

postgres

https://docs.yield.fi/lending

is the data good.. ? 


### Compound API
To use JSON in both the input and the output, specify the headers "Content-Type: application/json" and "Accept: application/json" in the request.

`fetch("https://api.compound.finance/api/v2/market_history/graph?asset=0xf5dce57282a584d2746faf1593d3121fcac444dc&min_block_timestamp=1556747900&max_block_timestamp=1559339900&num_buckets=10");`

for now API key not necessary

### dydx

### bxz, fulcrum
curl -X GET "https://api.bzx.network/v1/asset-stats-history?asset=eth&start_date=1600300800&end_date=1606112268&points_number=10" -H  "accept: application/json"
d


### aave
subgraph - reserve data

`LendingPoolCore`'s `updateReserveInterestRatesAndTimestampInternal()`


## prediction, decision
old window and new window averages. line and extrapolation between the two. best angle wins.



## movement of assets 
web3 contracts
back to ETH everytime

dydx - perpetual vs solo: 


## see also
- https://defirate.com/lend/
- https://idle.finance/
- https://yearn.finance/stats


## about the ABIs
couldn't load the 'old' Compound Comptroller ABI because it wasn't validating with web3py