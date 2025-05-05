import random
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