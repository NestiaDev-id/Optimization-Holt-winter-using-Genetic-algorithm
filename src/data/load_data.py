import pandas as pd
import os

def load_excel_data(file_path):
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    
    df = pd.read_excel(file_path)
    return df
