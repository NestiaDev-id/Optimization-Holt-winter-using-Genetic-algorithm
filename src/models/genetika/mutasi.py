# Fungsi Scramble Mutation
import random
from inisialisasi_populasi import to_binary
from inisialisasi_populasi import to_decimal
from models.holt_winters import holt
from models.evaluate import MAPE

def scramble_mutasi(train, test, populasi):
    # Gabungkan kromosom menjadi satu string
    parents1 = populasi['Alpha'] + populasi['Beta'] + populasi['Gamma']
    # print('Mutasi sebelum diproses: ', parents1)
    
    # Pilih dua titik acak untuk menentukan segmen yang akan diacak
    point1, point2 = sorted(random.sample(range(len(parents1)), 2))
    # print('Titik potong: ', point1, point2)
    
    # Pilih segmen yang akan diacak
    segment_to_scramble = parents1[point1:point2]
    # print('Segmen yang akan diacak: ', segment_to_scramble)
    
    # Acak urutan segmen
    scrambled_segment = ''.join(random.sample(segment_to_scramble, len(segment_to_scramble)))
    # print('Segmen setelah diacak: ', scrambled_segment)
    
    # Gabungkan kembali dengan segmen yang tidak berubah
    child1 = parents1[:point1] + scrambled_segment + parents1[point2:]
    # print('Kromosom anak setelah scramble: ', child1)

    # Pisahkan kembali menjadi Alpha, Beta, Gamma
    child1_data = {
        'Alpha': child1[:10],
        'Beta': child1[10:20],
        'Gamma': child1[20:30],
        'Fitness': None
    }

    # Mengubah biner ke desimal
    child1_data['Alpha'] = to_decimal(child1_data['Alpha'])
    child1_data['Beta'] = to_decimal(child1_data['Beta'])
    child1_data['Gamma'] = to_decimal(child1_data['Gamma'])

    # Hitung nilai fitness menggunakan Holt dan MAPE
    _, hasil_ramalan_child1, _ = holt(train, child1_data['Alpha'], child1_data['Beta'], child1_data['Gamma'])
    child1_data['Fitness'] = MAPE(test, hasil_ramalan_child1)

    # Ubah kembali ke biner
    child1_data['Alpha'] = to_binary(child1_data['Alpha'])
    child1_data['Beta'] = to_binary(child1_data['Beta'])
    child1_data['Gamma'] = to_binary(child1_data['Gamma'])

    # Kembalikan anak dengan fitness
    return {
        'Alpha': child1_data['Alpha'],
        'Beta': child1_data['Beta'],
        'Gamma': child1_data['Gamma'],
        'Fitness': child1_data['Fitness']
    }
    
def mutasi_swap(train, test, populasi):
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
