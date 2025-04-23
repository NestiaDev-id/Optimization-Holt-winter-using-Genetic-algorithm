import pandas as pd

def clean_data(df):
    """
    Membersihkan data seperti:
    - Menghapus kolom yang tidak diperlukan
    - Mengisi nilai kosong (NaN)
    - Menghapus duplikasi
    - Deteksi dan hapus outlier
    """
      
    # 1. Menghapus kolom yang tidak digunakan
    df = df.drop(columns=['bulan', 'tahun'], errors='ignore')

    # 2. Mengisi nilai kosong, kemudian digantikan dengan rata-rata
    df.fillna(df.mean(), inplace=True)

    # 3. Menghapus duplikasi
    df.drop_duplicates(inplace=True)

    # 4. Deteksi dan hapus outlier menggunakan IQR
    Q1 = df['jumlah'].quantile(0.25)
    Q3 = df['jumlah'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df = df[(df['jumlah'] >= lower_bound) & (df['jumlah'] <= upper_bound)]
    
    # Mengganti outlier dengan nilai mean
    mean_value = df['jumlah'].mean()
    df['jumlah'] = df['jumlah'].apply(lambda x: mean_value if x < lower_bound or x > upper_bound else x)

    return df
