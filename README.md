# interactivebrockers
The main goal of this repository is to test interactivebrockers API and see how it works  
My goals for the moment are:
* Create a hello world application (done)
* Collect historical market data for several instruments
* Create a dummy paper trading algorythm (it should by and sell at a random time). Later I will use him as a benchmark
* Create a mooving average trading algorythm

## Fetching the data
The code is stored in the fetch_candles folder. I use interactive brockers API to get data from forex for 3 pairs of currencies:  
* EUR-GBP
* EUR-USD
* EUR-JPY
  
For each of these pairs, we get 1 minute candles for 10 days. The data is stored in a txt file in the Data folder

## Dummy algo
The idea is simple, we buy and sell assets at random times. Run_test function generates a large number of random permutations of deals and estimates the mean and the standard deviation of deals inside this permutation.

## Mooving average
The idea is that for each data point we calculate 2 means:
* short term mean
* long term mean
  
If on a given moment the short term mean is higher than the long-term, this means that the trend is ascending and we need to buy if we have not already. If the short term mean is under the long term, then the trend is descending and we need to sell. In general, I will be searching for a moment these means alternate.  
Duration of long term and short term is not fixed. The idea is to find a combination of durations that fits the best into the given data.  
Still need to work on generalisation...