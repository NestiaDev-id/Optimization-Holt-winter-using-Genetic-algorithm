from inisialisasi_populasi import to_binary
from inisialisasi_populasi import to_decimal
from models.holt_winters import holt
from models.evaluate import MAPE

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
