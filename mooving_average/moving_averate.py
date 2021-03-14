from read_data import read_data_to_df

import numpy as np
import pandas as pd

import itertools

from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go



def buy_sell(data):
    '''
    function generates byuy/sell signals based on moving averages
    we will use the following trade states:
        open : for state when a position is open
            in this case we are looking for a moment, when 
    :data: dataset. should contain sma_short and sma_long columns
    :return: a tuple containing (buy, sell) prices
    '''
    sigPriceBuy = []
    sigPriceSell = []
    position_open = False

    for i in range(len(data)):
        if position_open:
            #if over recent periods the price is higher than over longterm, the trend in acsending
            #we keep the position openned
            if data.sma_short[i] > data.sma_long[i]:
                sigPriceBuy.append(None)
                sigPriceSell.append(None)
            #else, the trend has chaned and we need to close the position
            else:
                sigPriceBuy.append(None)
                sigPriceSell.append(data.open[i])
                position_open = False
        else:
            #the trend is accending. the asset costed more over recent periods than in longterm
            #we buy an assed
            if data.sma_short[i] > data.sma_long[i]:
                sigPriceBuy.append(data.open[i])
                sigPriceSell.append(None)
                position_open = True
            #The trend is descending. We wait for a moment to buy
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
    ds.columns = ["step","buy_signal_price","sell_signal_price"]
    n_deals = len(ds)//2

    if ds.buy_signal_price[0] is None:
        start = 1
    else:
        start = 0

    for i in range(start, n_deals, 2):       
        deal_profits.append([ds.step[i],
                             data.date[ds.step[i]],
                             ds.buy_signal_price[i],
                             ds.step[i+1],
                             data.date[ds.step[i+1]],
                             ds.sell_signal_price[i+1],
                             round(ds.sell_signal_price[i+1]-ds.buy_signal_price[i],6)])

    deal_profits = pd.DataFrame(deal_profits, columns=["step_bought",
                                                       "time_bought",
                                                       "rate_bought",
                                                       "step_sold",
                                                       "time_sold",
                                                       "rate_sold",
                                                       "profit"])
    return deal_profits


def show_strategy(path, len_long, len_short):
    df = read_data_to_df(path)
    deals = calculate_averages(df, len_long, len_short)
    eval_ds = evaluate_mooving_average_deals(deals)

    open_price = go.Scatter(
        x=df.date, y=df.open, 
        mode='lines', 
        connectgaps=False, 
        line=dict(color='firebrick', width=2),
        name="open price"
    )

    sma_short = go.Scatter(
        x=df.date,
        y=df.sma_short,
        mode="lines", 
        connectgaps=False, 
        line=dict(color='yellow', width=1),
        name="sma short"
    )

    sma_long = go.Scatter(
        x=df.date,
        y=df.sma_long,
        mode="lines", 
        connectgaps=False, 
        line=dict(color='green', width=1),
        name="sma long"
    )


    buy_markers = go.Scatter(
        x=deals.date,
        y=deals.buy_signal_price, 
        mode="markers", 
        marker_symbol = "cross",
        marker=dict(color="blue"),
        name="buy"
    )

    sell_markers = go.Scatter(
        x = deals.date,
        y = deals.sell_signal_price,
        mode="markers",
        marker=dict(color="red", symbol="diamond-wide"),
        name="sell"
    )

    fig = go.Figure(data=open_price)
    fig.add_trace(sma_short)
    fig.add_trace(sma_long)
    fig.add_trace(buy_markers)
    fig.add_trace(sell_markers)

    for pos, row in eval_ds.iterrows():
        if row.profit >0:
            rect_col = "green"
        else:
            rect_col = "red"

        fig.add_shape(
            type="rect",
            x0=row.time_bought,y0=row.rate_bought,x1=row.time_sold,y1=row.rate_sold,
            opacity=.2,
            fillcolor = rect_col
        )

    fig.show()
    # print(df)
    # print(deals)
    # print(eval_ds)
    return df, deals, eval_ds


def show_deals_plane(path, long_range, short_range, investment):
    '''
    Function evaluates expected outcome for moving average strategy 
    for a given path
    :path: path to the market data
    :long_range:
        expected a tuple with 3 values:
            start, end, step
    :short_range:
        expected a tuple with 3 values
            start, end, step
    :return: does not return anything. Just shows a heatmap with parameter values
    '''
    df = read_data_to_df(path)

    # generate permutations
    longs = [el for el in range(long_range[0], long_range[1], long_range[2])]
    shorts = [el for el in range(short_range[0], short_range[1], short_range[2])]
    permut = list(itertools.product(longs, shorts))

    deals_plane = []
    for el in permut:
        deals = calculate_averages(df, el[0], el[1])
        eval_ds = evaluate_mooving_average_deals(deals)
        deals_plane.append([np.sum(eval_ds.profit*investment), el[0], el[1]])

    deals_plane = pd.DataFrame(deals_plane, columns = ["profit","long", "short"])
    # print(deals_plane)

    fig = px.density_heatmap(deals_plane, x="long",y="short",z="profit")
    fig.show()

    return

def main():
    #read data
    path = "C:\\Users\\grego\\interactivebrockers\\data\\EurJpyFx.txt"
#    print(np.sum(eval_ds.profit*1000))

#for EUR GBP pair
#    show_deals_plane(path,[50,150,5],[5,45,5],1000)
#    show_deals_plane(path,[80,140,2],[10,20,1],1000)
#    show_deals_plane(path,[80,90,1],[11,14,1],1000)
#    show_deals_plane(path,[80,84,1],[13,14,1],1000)
#    df, deals, eval_ds = show_strategy(path, 80, 14)

#for EUR USD pair
#    show_deals_plane(path,[50,150,5],[5,45,5],1000)  
#    show_deals_plane(path,[120,130,1],[20,30,1],1000)
#    df, deals, eval_ds = show_strategy(path, 124, 20)

#for EUR JPY pair
    # show_deals_plane(path,[50,150,5],[5,45,5],1000)
    # show_deals_plane(path,[140,150,1],[40,50,1],1000)
    df, deals, eval_ds = show_strategy(path, 148, 49)




if __name__ == '__main__':
    main()