import random
from .holt_winters import holt
from .evaluate import MAPE

import sys
sys.set_int_max_str_digits(10240)


def to_binary(value, num_bits=10):
    # Mengalikan nilai dengan 1000 dan mengubahnya menjadi integer
    scaled_value = int(value * (2** num_bits))  
    # Mengubah integer menjadi representasi biner
    return bin(scaled_value)[2:].zfill(num_bits) 

def to_decimal(binary_value):
    return int(binary_value, 2) / (2 ** len(binary_value))  # Mengubah dari biner ke desimal

# Algoritma Genetika
def pembentukan_populasi_awal(jumlahKromosom):
    biner = []
    for i in range(jumlahKromosom):
        # Generate random number untuk alpha beta dan gamma
        alpha = random.uniform(0.01, 0.99)
        beta = random.uniform(0.01, 0.99)
        gamma = random.uniform(0.01, 0.99)
        # Mengubah alpha, beta, gamma ke format biner
        alpha_biner = to_binary(alpha)
        beta_biner = to_binary(beta)
        gamma_biner = to_binary(gamma)
        biner.append({
            'Alpha': alpha_biner,
            'Beta': beta_biner,
            'Gamma': gamma_biner,
            'Fitness': None
            })
    return biner

# Fungsi evaluasi_fitness tanpa print yang tidak diperlukan
def evaluasi_fitness(populasi, train, test):
    evaluasi_fitness = []
    
    for i, individu in enumerate(populasi):
        # Mengambil nilai alpha, beta, gamma dalam format biner
        alpha_biner = individu['Alpha']
        beta_biner = individu['Beta']
        gamma_biner = individu['Gamma']
        
        # Konversi nilai biner menjadi desimal
        alpha = to_decimal(alpha_biner)
        beta = to_decimal(beta_biner)
        gamma = to_decimal(gamma_biner)
        
        # Menggunakan nilai alpha, beta, gamma untuk melakukan peramalan
        _, hasil_ramalan, _ = holt(train, alpha, beta, gamma)
        
        # Hitung fitness berdasarkan MAPE
        individu['Fitness'] = MAPE(test, hasil_ramalan)
        
        # Ubah ke biner lagi
        alpha = to_binary(alpha)
        beta = to_binary(beta)
        gamma = to_binary(gamma)

        # Menyusun hasil evaluasi fitness untuk individu
        evaluasi_fitness.append({
            'Alpha': alpha,
            'Beta': beta,
            'Gamma': gamma,
            'Fitness': individu['Fitness']
        })

    return evaluasi_fitness    

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

def mutasi2(train, test, populasi):
    # Ubah bilangan menjadi biner
    # parents1 = {
    #     'Alpha': to_binary(populasi['Alpha']),
    #     'Beta': to_binary(populasi['Beta']),
    #     'Gamma': to_binary(populasi['Gamma'])
    # }

    # Gabungkan biner
    parents1 = populasi['Alpha'] + populasi['Beta'] + populasi['Gamma']
    # print('mutasi sebelum di proses: ',parents1)
    
    point1, point2 = sorted(random.sample(range(len(parents1)), 2))
    # print('Titik potong', point1, point2)

    
    # Balikkan segmen yang diinginkan
    reversed_segment = parents1[point1:point2][::-1]
    # print('reverse: ',reversed_segment, point1, point2)
    # print('parents1[point1:point2]: ',parents1[point1:point2])
    # Gabungkan kembali segmen-segmen menjadi child1
    child1 = parents1[:point1] + reversed_segment + parents1[point2:]
    # print('gabung anak mutasi: ',child1)
    # kromosom_reversed = parents1[::-1]  # Membalik string
    # print(kromosom_reversed)

    # Pisahkan kembali ke alpha, beta, gamma
    child1 = {
        'Alpha': child1[:10],
        'Beta': child1[10:20],
        'Gamma': child1[20:30],
        'Fitness': None
    }

    # Mengubah biner ke desimal
    child1['Alpha'] = to_decimal(child1['Alpha'])
    child1['Beta'] = to_decimal(child1['Beta'])
    child1['Gamma'] = to_decimal(child1['Gamma'])

    # Hitung nilai fitness menggunakan Holt dan MAPE
    _, hasil_ramalan_child1, _ = holt(train, child1['Alpha'], child1['Beta'], child1['Gamma'])
    
    child1['Fitness'] = MAPE(test, hasil_ramalan_child1)

    # ubah ke biner lagi
    child1['Alpha'] = to_binary(child1['Alpha'])
    child1['Beta'] = to_binary(child1['Beta'])
    child1['Gamma'] = to_binary(child1['Gamma'])
    
    return {
        'Alpha': child1['Alpha'],
        'Beta': child1['Beta'],
        'Gamma': child1['Gamma'],
        'Fitness': child1['Fitness']
    }

def crossover(train, test, parents1, parents2):
    # Ubah bilangan menjadi biner
    print(parents1)
    print(parents2)
    parents1 = {
        'Alpha': to_binary(parents1['Alpha']),
        'Beta': to_binary(parents1['Beta']),
        'Gamma': to_binary(parents1['Gamma'])
    }
    parents2 = {
        'Alpha': to_binary(parents2['Alpha']),
        'Beta': to_binary(parents2['Beta']),
        'Gamma': to_binary(parents2['Gamma'])
    }
    

    # Gabungkan biner
    parents1 = parents1['Alpha'] + parents1['Beta'] + parents1['Gamma']
    parents2 = parents2['Alpha'] + parents2['Beta'] + parents2['Gamma']

    # Menentukan titik potong
    point1, point2 = sorted(random.sample(range(len(parents1)), 2))
    # print(f"Titik potong: {point1}, {point2}")

    # Membagi berdasarkan titik potong
    bagian1_child1 = parents1[:point1] + parents2[point1:point2] + parents1[point2:]
    bagian1_child2 = parents2[:point1] + parents1[point1:point2] + parents2[point2:]

    # Pisahkan kembali ke alpha, beta, gamma
    child1 = {
        'Alpha': bagian1_child1[:10],
        'Beta': bagian1_child1[10:20],
        'Gamma': bagian1_child1[20:30],
        'Fitness': None
    }
    child2 = {
        'Alpha': bagian1_child2[:10],
        'Beta': bagian1_child2[10:20],
        'Gamma': bagian1_child2[20:30],
        'Fitness': None
    }
    

    # Mengubah biner ke desimal
    child1['Alpha'] = to_decimal(child1['Alpha'])
    child1['Beta'] = to_decimal(child1['Beta'])
    child1['Gamma'] = to_decimal(child1['Gamma'])

    child2['Alpha'] = to_decimal(child2['Alpha'])
    child2['Beta'] = to_decimal(child2['Beta'])
    child2['Gamma'] = to_decimal(child2['Gamma'])

    _, hasil_ramalan_child1, _ = holt(train, child1['Alpha'], child1['Beta'], child1['Gamma'])
    _, hasil_ramalan_child2, _ = holt(train, child2['Alpha'], child2['Beta'], child2['Gamma'])
    
    child1['Fitness'] = MAPE(test, hasil_ramalan_child1)
    child2['Fitness'] = MAPE(test, hasil_ramalan_child2)

    # Mengubah ke biner lagi
    child1['Alpha'] = to_binary(child1['Alpha'])
    child1['Beta'] = to_binary(child1['Beta'])
    child1['Gamma'] = to_binary(child1['Gamma'])

    child2['Alpha'] = to_binary(child2['Alpha'])
    child2['Beta'] = to_binary(child2['Beta'])
    child2['Gamma'] = to_binary(child2['Gamma'])

    # print('Anak 1', child1['Alpha'], child1['Beta'], child1['Gamma'], child1['Fitness'])
    # print('Anak 2', child2['Alpha'], child2['Beta'], child2['Gamma'], child2['Fitness'])

    # Mengembalikan 2 anak
    return {
        'Alpha': child1['Alpha'],
        'Beta': child1['Beta'],
        'Gamma': child1['Gamma'],
        'Fitness': child1['Fitness']
    }, {
        'Alpha': child2['Alpha'],
        'Beta': child2['Beta'],
        'Gamma': child2['Gamma'],
        'Fitness': child2['Fitness']
    }


    # Mengembalikan anak dengan fitness lebih kecil
    # if child1['Fitness'] < child2['Fitness']:
    #     return {
    #     'Alpha': child1['Alpha'],
    #     'Beta': child1['Beta'],
    #     'Gamma': child1['Gamma'],
    #     'Fitness': child1['Fitness']
    # }
    # else:
    #     return {
    #     'Alpha': child2['Alpha'],
    #     'Beta': child2['Beta'],
    #     'Gamma': child2['Gamma'],
    #     'Fitness': child2['Fitness']
    # }

def algoritma_genetika6(train, test,  jumlahKromosom, generations, probability):
    no_improvement_count = 0
    best_fitness_overall = float('inf')  # Inisialisasi dengan nilai fitness maksimum
    fitness_history = []

    # Membentuk populasi awal
    populasi = pembentukan_populasi_awal(jumlahKromosom)
    print(f'Pembentukan populasi awal: ', populasi)

    for generasi in range(generations):
        print(f"\nIterasi ke-{generasi + 1}")

        # Evaluasi fitness populasi
        print(f"Populasi: {populasi}")
        fitness_values = evaluasi_fitness(populasi, train, test)
        print(f'Fitness values: ', fitness_values)
        
        # Mengambil hanya fitness yang lebih besar dari 0
        fitness_values_positive = [individu for individu in fitness_values if individu['Fitness'] > 0]

        # Cari individu terbaik dalam populasi saat ini
        best_individu_generasi = min(fitness_values_positive, key=lambda x: x['Fitness'])
        print(f'best individu generasi ke-{generasi + 1}: {best_individu_generasi}')

        # Tambahkan fitness terbaik ke dalam history
        fitness_history.append(best_individu_generasi['Fitness'])
        print(f"Fitness Terbaik Generasi ini: {best_individu_generasi['Fitness']}")

        # Simpan individu terbaik secara keseluruhan
        if best_individu_generasi['Fitness'] < best_fitness_overall:
            best_fitness_overall = best_individu_generasi['Fitness']
            best_individu_overall = best_individu_generasi.copy()
            no_improvement_count = 0
        else:
            no_improvement_count += 1
        
        # Tambahkan individu acak jika tidak ada perbaikan selama 10 generasi berturut-turut
        if no_improvement_count >= 10:
            print("Tidak ada perbaikan, menghapus individu dan menambahkan individu secara acak.")

            # Elite individu mempertahankan individu terbaik
            # Jumlah individu yang akan dihapus skitar 80% dari jumlah kromosom
            # Menghapus 8 individu dari jumlah kromosom 10
            size = int(jumlahKromosom * 0.8)  
            # Simpan individu terbaik (elitisme)
            elite_individuals = populasi[:size]  # Pertahankan individu terbaik
            
            # Hapus individu dengan performa terburuk dari populasi
            populasi = sorted(populasi, key=lambda x: x['Fitness'])[:jumlahKromosom]
            populasi = populasi[:-size]  # Hapus individu dari bagian akhir
            
            # Tambahkan individu acak untuk menggantikan individu yang dihapus
            populasi = elite_individuals + pembentukan_populasi_awal(jumlahKromosom - len(elite_individuals))
            
            # Evaluasi kembali fitness populasi setelah perubahan
            fitness_values = evaluasi_fitness(populasi, train, test)

            # Reset penghitung no improvement
            no_improvement_count = 0

        # Membentuk populasi baru
        new_populasi = []

        # Tambahkan individu terbaik ke populasi baru (elitisme)
        new_populasi.append(best_individu_generasi)

        # Proses seleksi, crossover, dan mutasi untuk membentuk sisa populasi
        # Selama jumlah individu dalam populasi baru lebih kecil dari jumlah kromosom yang ditentukan,
        # maka akan dilakukan proses seleksi pasangan induk, crossover, dan mutasi untuk menghasilkan keturunan.
        while len(new_populasi) < jumlahKromosom:
            # Seleksi individu dari populasi saat ini menggunakan metode Roulette Wheel
            parent1 = RouletteWhell(fitness_values)  # Pilih induk pertama
            parent2 = RouletteWhell(fitness_values)  # Pilih induk kedua
 
            # Crossover: Menggabungkan dua induk untuk menghasilkan dua keturunan
            offspring1, offspring2 = crossover(train, test, parent1, parent2)

            # Mutasi: Memodifikasi gen keturunan secara acak berdasarkan probabilitas tertentu
            if generasi % probability == 0:  # Jika generasi memenuhi syarat probabilitas untuk mutasi
                offspring1 = mutasi2(train, test, offspring1)
                offspring2 = mutasi2(train, test, offspring2)

            # Evaluasi fitness keturunan baru
            fitness_values_offspring = evaluasi_fitness([offspring1, offspring2], train, test)
            # print(fitness_values_offspring)
            # print('offspring1: ',offspring1)
            # print('offspring2: ',offspring2)
            # Tambahkan keturunan ke populasi baru
            new_populasi.extend([offspring1, offspring2])
            
        # Pastikan populasi baru tidak melebihi ukuran yang ditentukan
        # Jika jumlah individu dalam new_populasi lebih dari jumlahKromosom, kelebihannya akan dibuang.
        populasi = new_populasi[:jumlahKromosom]

    # Individu terbaik setelah semua generasi
    best_individu_overall = {
        'Alpha': to_decimal(best_individu_overall['Alpha']),
        'Beta': to_decimal(best_individu_overall['Beta']),
        'Gamma': to_decimal(best_individu_overall['Gamma']),
        'Fitness': best_individu_overall['Fitness'],
    }

    print(f"\nIndividu Terbaik di Seluruh Generasi: {best_individu_overall}")
    return best_individu_overall, generations, fitness_history
