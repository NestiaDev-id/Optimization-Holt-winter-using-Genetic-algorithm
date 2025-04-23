import pandas as pd
from sklearn.preprocessing import StandardScaler

def select_features(df, target_column=None):
    """
    Memilih fitur yang relevan dari DataFrame.
    
    Args:
        df (pd.DataFrame): Dataset
        target_column (str): Kolom target, jika ada

    Returns:
        pd.DataFrame: DataFrame dengan fitur terpilih
    """
    # Misalnya, buang kolom yang tidak berguna atau yang memiliki terlalu banyak missing value
    df = df.dropna(thresh=0.5*len(df), axis=1)  # Hapus kolom dengan lebih dari 50% missing

    if target_column:
        features = df.drop(columns=[target_column])
    else:
        features = df.copy()

    return features


def scale_features(X):
    """
    Normalisasi fitur numerik dengan StandardScaler

    Args:
        X (pd.DataFrame): Fitur numerik

    Returns:
        pd.DataFrame: Fitur yang sudah dinormalisasi
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return pd.DataFrame(X_scaled, columns=X.columns)
