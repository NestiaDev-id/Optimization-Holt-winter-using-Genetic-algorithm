from inisialisasi_populasi import to_binary
from inisialisasi_populasi import to_decimal
import random
from models.holt_winters import holt
from models.evaluate import MAPE

def uniform_crossover(train, test, parent1, parent2):
    # Ubah bilangan menjadi biner
    parent1 = {
        'Alpha': to_binary(parent1['Alpha']),
        'Beta': to_binary(parent1['Beta']),
        'Gamma': to_binary(parent1['Gamma'])
    }
    parent2 = {
        'Alpha': to_binary(parent2['Alpha']),
        'Beta': to_binary(parent2['Beta']),
        'Gamma': to_binary(parent2['Gamma'])
    }

    # Gabungkan biner menjadi satu string (untuk crossover)
    parent1 = parent1['Alpha'] + parent1['Beta'] + parent1['Gamma']
    parent2 = parent2['Alpha'] + parent2['Beta'] + parent2['Gamma']

    # Uniform crossover: Setiap gen diambil dari salah satu parent secara acak
    child1 = ''.join(random.choice([parent1[i], parent2[i]]) for i in range(len(parent1)))
    child2 = ''.join(random.choice([parent1[i], parent2[i]]) for i in range(len(parent2)))

    # Pisahkan kembali ke Alpha, Beta, Gamma
    child1_data = {
        'Alpha': child1[:10],
        'Beta': child1[10:20],
        'Gamma': child1[20:30],
        'Fitness': None
    }

    child2_data = {
        'Alpha': child2[:10],
        'Beta': child2[10:20],
        'Gamma': child2[20:30],
        'Fitness': None
    }

    # Mengubah biner ke desimal
    child1_data['Alpha'] = to_decimal(child1_data['Alpha'])
    child1_data['Beta'] = to_decimal(child1_data['Beta'])
    child1_data['Gamma'] = to_decimal(child1_data['Gamma'])

    child2_data['Alpha'] = to_decimal(child2_data['Alpha'])
    child2_data['Beta'] = to_decimal(child2_data['Beta'])
    child2_data['Gamma'] = to_decimal(child2_data['Gamma'])

    # Hasil ramalan dengan Holt
    _, hasil_ramalan_child1, _ = holt(train, child1_data['Alpha'], child1_data['Beta'], child1_data['Gamma'])
    _, hasil_ramalan_child2, _ = holt(train, child2_data['Alpha'], child2_data['Beta'], child2_data['Gamma'])

    # Menghitung fitness menggunakan MAPE
    child1_data['Fitness'] = MAPE(test, hasil_ramalan_child1)
    child2_data['Fitness'] = MAPE(test, hasil_ramalan_child2)

    # Kembalikan ke bentuk biner
    child1_data['Alpha'] = to_binary(child1_data['Alpha'])
    child1_data['Beta'] = to_binary(child1_data['Beta'])
    child1_data['Gamma'] = to_binary(child1_data['Gamma'])

    child2_data['Alpha'] = to_binary(child2_data['Alpha'])
    child2_data['Beta'] = to_binary(child2_data['Beta'])
    child2_data['Gamma'] = to_binary(child2_data['Gamma'])

    # Mengembalikan 2 anak
    return child1_data, child2_data


def crossover_two_point(train, test, parents1, parents2):
    # Ubah bilangan menjadi biner
    # print(parents1)
    # print(parents2)
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
