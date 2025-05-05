import random

def Tournament(populasi, k=None):
    # Jika k tidak diberikan, set k sebagai 2 untuk memilih 2 individu acak
    if k is None:
        k = max(2, len(populasi) // 10)  # Pilih k=10% dari populasi, minimal k=2
    
    # Pastikan k tidak melebihi ukuran populasi
    k = min(k, len(populasi))

    # Acak pemilihan individu untuk turnamen
    tournament_pool = random.sample(populasi, k)

    # Pilih individu dengan fitness terbaik (terkecil)
    winner = min(tournament_pool, key=lambda x: x['Fitness'])  # Lebih kecil fitness lebih baik

    return winner

def RankSelection(populasi):
    # Urutkan populasi berdasarkan fitness (fitness lebih kecil lebih baik)
    populasi_terurut = sorted(populasi, key=lambda x: x['Fitness'])
    
    # Hitung total peringkat
    total_rank = sum(range(1, len(populasi) + 1))
    
    # Hitung peluang seleksi berdasarkan peringkat
    fitness_relatif = []
    for i in range(len(populasi)):
        rank = i + 1  # Peringkat individu (1 untuk yang terbaik)
        fitness_relatif.append(rank / total_rank)  # Probabilitas seleksi
    
    # Pilih individu berdasarkan probabilitas peringkat
    r = random.random()
    cumulative_probability = 0.0
    
    for i, prob in enumerate(fitness_relatif):
        cumulative_probability += prob
        if r <= cumulative_probability:
            return populasi_terurut[i]


def RouletteWhell(populasi):
    fitness_balik = []
    fitness_relatif = []
    fitness_kumulatif = []
    
    for individu in populasi:
        # proses pembalikan
        hitung_pembalik = 1 / individu['Fitness']
        fitness_balik.append(hitung_pembalik)


    total_fitness_balik = sum(fitness_balik)
    
    # hitung fitnes relatif
    for i in range(len(populasi)):
        hitung_relatif = fitness_balik[i] / total_fitness_balik
        fitness_relatif.append(hitung_relatif)

    # hitung fitness kumulatif
    for i in range(len(populasi)):
        if i == 0:
            hitung_kumulatif = 0 + fitness_relatif[i]
        else:
            hitung_kumulatif = fitness_kumulatif[i - 1] + fitness_relatif[i]
        fitness_kumulatif.append(hitung_kumulatif)

    # print("Fitness relatif:", fitness_relatif)
    # print("Fitness kumulatif:", fitness_kumulatif)

    r1 = random.random()
    
    for i, cumulative_probability in enumerate(fitness_kumulatif):
        if r1 <= cumulative_probability:
            return populasi[i]
