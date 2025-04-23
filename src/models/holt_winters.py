import numpy as np

def holt(df, alpha, beta, gamma):
    # Mengambil data 'jumlah' sebagai input dari dataframe
    data = df['jumlah'].tolist()
    # print('data training: ',data)
    periode_musim = 12  # Jumlah periode musim (misalnya 12 bulan)
    jumlah_data_uji = len(data)  # Jumlah data uji yang diinginkan
    # print(jumlah_data_uji)
    jumlah_prediksi = 12  # Jumlah prediksi ke depan

    # Data uji yang dimulai setelah periode musim
    data_uji = data[:jumlah_data_uji]
    print(f'data training: {data_uji}')

    # Menghitung nilai awal untuk level (L), tren (b), dan musiman (S)
    data_awal = data[:periode_musim]
    nilai_musiman_awal = [data_uji[i] / np.mean(data_uji[:periode_musim]) for i in range(periode_musim)]
    # print("Nilai musiman awal: ", nilai_musiman_awal)

    # Inisialisasi level dan tren awal
    level_awal = (1 / periode_musim)* sum(data_awal)
    tren_awal = (1/periode_musim) * sum([(data_uji[i + periode_musim] - data_uji[i]) / periode_musim for i in range(periode_musim)])

    # List untuk menyimpan hasil perhitungan
    level = [level_awal]
    tren = [tren_awal]
    musiman = nilai_musiman_awal.copy()

    # Debugging nilai awal
    print("Level awal:", level_awal)
    print("Tren awal:", tren_awal)
    print("Musiman awal:", nilai_musiman_awal)
    temp_musiman = []

    # Iterasi untuk menghitung level, tren, dan musiman
    for i in range(periode_musim, jumlah_data_uji):
        indeks_musiman = i % periode_musim  # Indeks musiman (reset setelah 12)
        # print(musiman)
        # Menghitung level
        L = alpha * (data_uji[i] / musiman[indeks_musiman]) + (1 - alpha) * (level[-1] + tren[-1])
        level.append((L))

        # Menghitung tren
        b = beta * (L - level[-2]) + (1 - beta) * tren[-1]
        tren.append(b)

        # Menghitung nilai musiman baru
        S = gamma * (data_uji[i] / L) + (1 - gamma) * musiman[indeks_musiman]
        # musiman[indeks_musiman] = round(S, 2)  # Perbarui nilai musiman pada indeks yang sesuai
        temp_musiman.append(S)
        # musiman.append(S)
        
        # Debugging per iterasi
        # print(f"Iterasi ke-{i - periode_musim + 1}:")
        # print(f"  Data Uji[{i}]: {data_uji[i]}")
        # print(f"  Level (L): {L:.2f}")
        # print(f"  Tren (b): {b:.2f}")
        # print(f"  Musiman[{temp_musiman}]: {S}\n")
        # print(f"  Musiman[{indeks_musiman}]: {S:.2f}\n")
        # print(f"  Musiman[{indeks_musiman}]: {S}\n")

    # print("Nilai Level : ", level)
    # print("Mengecek dimensi Level : ", len(level))
    # print("Nilai Tren : ", tren)
    # print("Mengecek dimensi Tren : ", len(tren))
    # print("Nilai Musiman : ", temp_musiman)
    # print("Mengecek dimensi Musiman : ", len(temp_musiman))
    # print("Nilai indeks musiman : ", indeks_musiman, )

    ramalan = []
    for i in range(jumlah_prediksi):
        # Prediksi
        
        # print("level: ", level[180], "tren", tren[180], "Dikali", (i+1), "temp_musiman", temp_musiman[168+i])
        prediksi = ((level[180] + (tren[180]* (i+1) )) * temp_musiman[168 + i])
        # prediksi = (level[-1] + tren[-1] * (i + 1)) * temp_musiman[i]
        ramalan.append(prediksi)
        # print(f"Prediksi iterasi ke-{i+1}: {prediksi}")   
    
    # Menentukan periode ramalan dan data uji
    periode_uji = data_uji
    ramalan_periode = ramalan[:len(data_uji)]  # Menyesuaikan panjang ramalan dengan data uji

    # Melakukan prediksi ke depan sebanyak jumlah_prediksi periode
    prediksi_ke_depan = []
    for i in range(jumlah_prediksi):
        L = level[-1] + (i + 1) * tren[-1]
        S = nilai_musiman_awal[-periode_musim + (i % periode_musim)]
        prediksi = round(L * S)
        prediksi_ke_depan.append(prediksi)

    return periode_uji, ramalan_periode, prediksi_ke_depan

