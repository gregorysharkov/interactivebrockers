from read_data import read_data_to_df

import numpy as np
import pandas as pd

import itertools

from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px


def buy_sell(data):
    '''
    function generates byuy/sell signals based on moving averages
    :data: dataset. should contain sma_short and sma_long columns
    :return: a tuple containing (buy, sell) prices
    '''
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data.sma_short[i] > data.sma_long[i]:
            if flag != 1:
                sigPriceBuy.append(data.open[i])
                sigPriceSell.append(None)
                flag = 1
            else:
                sigPriceBuy.append(None)
                sigPriceSell.append(None)
        elif data.sma_short[i] < data.sma_long[i]:
            if flag != 0:
                sigPriceBuy.append(None)
                sigPriceSell.append(data.open[i])
                flag = 0
            else:
                sigPriceBuy.append(None)
                sigPriceSell.append(None)
        else:
            sigPriceBuy.append(None)
            sigPriceSell.append(None)

    return (sigPriceBuy, sigPriceSell)


def calculate_averages(data, len_long, len_short):
    '''
    function calculates moving average indicators of a given dataset
    :data: dataset. should contain open, and date columns
    :return: 
    '''
    # moving average for the last 30 mi
    sma_short = pd.DataFrame()
    sma_short["open"] = data.open.rolling(window=len_short).mean()

    #logn term eaverage for 100 min
    sma_long = pd.DataFrame()
    sma_long["open"] = data.open.rolling(window=len_long).mean()

    data["sma_short"] = sma_short.open
    data["sma_long"] = sma_long.open

    data = data[["date", "open", "sma_short", "sma_long"]]

    deals = buy_sell(data)
    data["buy_signal_price"] = deals[0]
    data["sell_signal_price"] = deals[1]

    return data


def evaluate_mooving_average_deals(data):
    '''
    function evaluates deals made by mooving average algorythm
    :data: 
    :return: a list of profits for each deal
    '''
    deal_profits = []

    ds = data.\
        loc[(data.buy_signal_price.notna())|(data.sell_signal_price.notna()),:].\
        reset_index()[["index","buy_signal_price","sell_signal_price"]]

    n_deals = len(ds)//2

    for i in range(0, n_deals, 2):       
        deal_profits.append([ds.index[i],
                             ds.buy_signal_price[i],
                             ds.index[i+1],
                             ds.buy_signal_price[i]/ds.sell_signal_price[i+1],
                             round(ds.buy_signal_price[i]/ds.sell_signal_price[i+1]-1,6)])

    deal_profits = pd.DataFrame(deal_profits, columns=["step_bought",
                                                       "rate_bought",
                                                       "step_sold",
                                                       "rate_sold",
                                                       "profit"])
    return deal_profits


def show_strategy(path, len_long, len_short):
    df = read_data_to_df(path)
    deals = calculate_averages(df, len_long, len_short)
    eval_ds = evaluate_mooving_average_deals(deals)
    print(deals)
    print(eval_ds)
    return


def main():
    #read data
    path = "C:\\Users\\grego\\interactivebrockers\\data\\EurUsdFx.txt"
    show_strategy(path, 50, 10)
    # df =  read_data_to_df(path)

    # # generate permutations
    # longs = [el for el in range(150, 200, 10)]
    # shorts = [el for el in range(30, 110, 10)]
    # permut = list(itertools.product(longs, shorts))

    # deals_plane = []
    # for el in permut:
    #     deals = calculate_averages(df, el[0], el[1])
    #     eval_ds = evaluate_mooving_average_deals(deals)
    #     deals_plane.append([eval_ds.profit.sum()*2000, el[0], el[1]])

    # deals_plane = pd.DataFrame(deals_plane, columns = ["profit","long", "short"])
    # print(deals_plane)

    # fig = px.density_heatmap(deals_plane, x="long",y="short",z="profit")
    # fig.show()

if __name__ == '__main__':
    main()