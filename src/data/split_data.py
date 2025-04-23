import pandas as pd

def time_series_split(df):
    """
    Membagi data ke dalam train dan test.
    """
    
    # Bagi data 90 persent ke train dan 10 persent ke test
    train = df[['jumlah']][:203]
    test = df[['jumlah']][203:216]
    
    train_list = train['jumlah'].tolist()
    test_list = test['jumlah'].tolist()
    
    return train_list, test_list