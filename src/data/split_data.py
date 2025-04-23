import pandas as pd

def time_series_split(df):
    """
    Membagi data ke dalam train dan test.
    """
    
    # Bagi data 90 persent ke train dan 10 persent ke test
    train = df[['jumlah']][:204]
    test = df[['jumlah']][204:216]
    
    return train, test