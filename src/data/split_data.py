import pandas as pd

def time_series_split(df, date_column='tanggal', split_date='2022-01-01'):
    """
    Membagi data ke dalam train dan test.
    """
    
    # Bagi data 90 persent ke train dan 10 persent ke test
    train = df['jumlah'][12:].copy()
    test = df.tail(12).copy()
    
    return train, test