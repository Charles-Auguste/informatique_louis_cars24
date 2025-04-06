from typing import Union
from pathlib import Path
import pandas as pd


def read_data(datapath: Union[str, Path]):
    datapath = Path(datapath)
    assert datapath.is_file(), "Your file does not exist"
    if datapath.suffix == ".xlsx":
        df = pd.read_excel(datapath)
    elif datapath.suffix == ".csv":
        df1 = pd.read_csv(datapath, sep=",", nrows=2)
        df2 = pd.read_csv(datapath, sep=";", nrows=2)
        if len(df1.columns) > len(df2.columns):
            df = pd.read_csv(datapath, sep=",")
        if len(df2.columns) > len(df1.columns):
            df = pd.read_csv(datapath, sep=";")
        elif len(df1.columns) == len(df2.columns):
            raise ValueError("Cannot read the .csv file (No matching separator)")
    else:
        raise ValueError("Cannot read the file (Unknown format)")

    return df
