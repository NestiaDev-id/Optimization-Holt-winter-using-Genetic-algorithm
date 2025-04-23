import pandas as pd

def clean_data(df):
    """
    Membersihkan data dengan langkah-langkah umum seperti:
    - Menghapus kolom yang tidak diperlukan
    - Mengisi nilai kosong (NaN)
    - Mengubah tipe data
    - Menghapus duplikasi
    
    Args:
        df (pd.DataFrame): Data yang perlu dibersihkan

    Returns:
        pd.DataFrame: Data yang sudah dibersihkan
    """
    
    # 1. Menghapus kolom yang tidak perlu (ubah sesuai kolom yang ada di datasetmu)
    df = df.drop(columns=['col_to_remove_1', 'col_to_remove_2'], errors='ignore')  # Ganti dengan nama kolom yang tidak diperlukan

    # 2. Mengisi nilai kosong dengan rata-rata atau median (misalnya)
    df.fillna(df.mean(), inplace=True)

    # 3. Menghapus duplikasi
    df.drop_duplicates(inplace=True)

    # 4. Mengubah tipe data jika diperlukan
    # df['column_name'] = df['column_name'].astype('int')  # Ganti sesuai kebutuhan

    return df
