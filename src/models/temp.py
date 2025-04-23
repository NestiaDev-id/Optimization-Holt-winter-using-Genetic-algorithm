def algoritma_genetika6(train, test,  jumlahKromosom, generations, probability):
    no_improvement_count = 0
    best_fitness_overall = float('inf')
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
        print(f"Daftar fitness setelah filter: ", fitness_values_positive)

        # Cari individu terbaik dalam populasi saat ini
        best_individu_generasi = min(fitness_values_positive, key=lambda x: x['Fitness'])
        print(f'best individu generasi ke-{generasi + 1}: {best_individu_generasi}')

        # Tambahkan fitness terbaik ke dalam history
        fitness_history.append(best_individu_generasi['Fitness'])
        print(f"Fitness Terbaik Generasi ini: {best_individu_generasi['Fitness']}")

        # Metode elitis, mempertahankan 
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
            print("fitness_values_offspring: ",fitness_values_offspring)
            # print('offspring1: ',offspring1)
            # print('offspring2: ',offspring2)
            # Tambahkan keturunan ke populasi baru
            # new_populasi.extend([offspring1, offspring2])
            


            # new_populasi.extend(fitness_positif)
            
        # Pastikan populasi baru tidak melebihi ukuran yang ditentukan
        # Jika jumlah individu dalam new_populasi lebih dari jumlahKromosom, kelebihannya akan dibuang.
        populasi = new_populasi[:jumlahKromosom]
    print(f"berikut daftar populasi",populasi)

    # Individu terbaik setelah semua generasi
    best_individu_overall = {
        'Alpha': to_decimal(best_individu_overall['Alpha']),
        'Beta': to_decimal(best_individu_overall['Beta']),
        'Gamma': to_decimal(best_individu_overall['Gamma']),
        'Fitness': best_individu_overall['Fitness'],
    }

    print(f"\nIndividu Terbaik di Seluruh Generasi: {best_individu_overall}")
    return best_individu_overall, generations, fitness_history