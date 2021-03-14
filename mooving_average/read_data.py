import pandas as pd
from datetime import datetime


def read_data_to_df(path):
    """
    function reads canndle data from a txt file into a pandas dataframe
    :paht: string containing the path to the csv file
    :return: a pandas dataframe containing date, open, high
    """

    with open(path, "r") as f:
        lines = f.readlines()

    lines = [x.strip().split(", ")[0:5] for x in lines]
    lines = [[x.split(": ")[-1] for x in elements] for elements in lines]
    ds = pd.DataFrame(lines, columns = ["date","open","high","low","close"])
    ds.date = pd.to_datetime(ds.date, format="%Y%m%d  %H:%M:%S")
    ds.set_index("date")

    numeric_cols = ["open","high","low","close"]
    ds[numeric_cols] = ds[numeric_cols].apply(pd.to_numeric, errors='coerce')

    return ds


def main():
    path = "C:\\Users\\grego\\interactivebrockers\\data\\EurGbpFx.txt"
    ds =  read_data_to_df(path)
    print(ds.dtypes)
    
    return

if __name__ == '__main__':
    main()
