# Fungsi MAPE untuk menghitung akurasi prediksi
def MAPE(data_test, hasil_ramalan):
    total_error = 0
    for i in range(len(data_test)):
        # print('data test', data_test[i], 'hasil ramalan', hasil_ramalan[i], '')
        total_error += abs(data_test[i] - hasil_ramalan[i]) / data_test[i]
    return (total_error / len(data_test)) * 100

def MAPE_setiap_periode(data_test, hasil_ramalan):
    mape_per_periode = []  # List untuk menyimpan MAPE per periode
    for i in range(len(data_test)):
        mape_periode = abs(data_test[i] - hasil_ramalan[i]) / data_test[i] * 100
        mape_per_periode.append(mape_periode)

    return mape_per_periode
