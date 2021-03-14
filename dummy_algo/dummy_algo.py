import pandas as pd
import random
import statistics as s
from datetime import datetime
import plotly.graph_objects as go
from read_data import read_data_to_df


def calculate_start_end(start, idle_times, open_times):
    """
    Function calculates start and end times based on idle and open_times intervals
    """
    n_intervals = len(idle_times)
    current_time = start
    positions = []
    for i in range(n_intervals):
        buy_time = current_time + idle_times[i]
        sell_time = buy_time + open_times[i]
        current_time = sell_time
        positions.append([buy_time, sell_time])

    return positions


def get_prices(pair, data):
    """
    function extracts data from a data set
    """
    open_time = data.loc[pair[0],"date"]
    close_time = data.loc[pair[1],"date"]
    buy_price = data.loc[pair[0],"open"]
    sell_price = data.loc[pair[1],"close"]
    profit = sell_price - buy_price
    return [open_time, close_time, buy_price, sell_price, profit]


def evaluate_permutation(data, n_perm, n_trades, investment=1000, max_idle=5, max_open=5):
    """
    function generates a random permutation and calculates its profit or loss
    :data: data frame containing stock information
    :n_perm: number of permutations (each with its own start time as well as with its own trade intervals)
    :n_trades: number of trades to be generated for each permutaion
    :return: a single number containing cumulative profit or loss
    """
    start = random.randint(1, 10)
    idle_time = [random.randrange(1,max_idle) for x in range(0,n_trades)]
    open_time = [random.randrange(1,max_open) for p in range(0,n_trades)]

    start_end_pair = calculate_start_end(start, idle_time, open_time)
    lines = pd.DataFrame([get_prices(x, data) for x in start_end_pair],
                         columns=["open_time","close_time","buy_price","sell_price","profit"])
    lines["profit_per_investment"] = lines.profit*investment
    return round(lines.profit_per_investment.sum(),4)


def run_test(path, seed, n_run, n_perm, n_trades, investment, give_me_profits=False):
    """
    function takes a dataset, generates a number of permutations, emulating opening and closing positions
    at a random interval. it returns average, standard deviation and the total sum of these deals
    :path: path to the file containing trade data
    :seed: seed for reproducibility
    :n_run: number of runs the whole test is repeated
    :n_perm: number of permutations created (each permutaion emulates one algoritm run)
    :n_trades: number of trades per run
    :investment: amount of money to be invested at each run
    """
    df =  read_data_to_df(path)

    random.seed(seed)
    profits = []
    for i in range(n_run):
        profits.append(evaluate_permutation(df, n_perm, n_trades, investment))

    print(f"Mean: {s.mean(profits)},\tSD: {s.stdev(profits)},\t sum: {sum(profits)}")
    if give_me_profits:
        return profits

    return

def main():
    paths = {"EUR GBP": "C:\\Users\\grego\\interactivebrockers\\data\\EurGbpFx.txt",
             "EUR USD": "C:\\Users\\grego\interactivebrockers\data\EurUsdFx.txt",
             "EUR JPY": "C:\\Users\\grego\\interactivebrockers\\data\\EurJpyFx.txt"}
             
    for key, value in paths.items():
        print(key)
        run_test(
            path = value,
            seed = 1983,
            n_run = 1000,
            n_perm = 1000,
            n_trades = 200,
            investment = 1000
        )
    return

if __name__ == '__main__':
    main()
