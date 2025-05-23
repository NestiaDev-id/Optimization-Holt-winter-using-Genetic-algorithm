from src.models.evaluate import MAPE
from src.models.ga_optimizer import algoritma_genetika6, to_decimal
from src.models.holt_winters import holt
from src.data.load_data import load_excel_data
from src.data.clean_data import clean_data
from src.data.split_data import time_series_split
from app.models.data_model import PredictionInput, PredictionResult
import sys
import os

# sys.path.append(os.path.abspath('../src'))

def predict_passenger(input_data: PredictionInput):
    # Load data
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) 
    file_path = os.path.join(base_path, 'data', 'raw', 'dataset original.xlsx')
    file_path2 = os.path.join(base_path, 'data', 'raw', 'dataset luar.xlsx')
    print(f"File path: {file_path}")
    df = load_excel_data(file_path)
    df2 = load_excel_data(file_path2)

    # Clean data
    df_cleaned = clean_data(df)
    df_cleaned2 = clean_data(df2)

    # Split
    train, test = time_series_split(df_cleaned)
    train2, test2 = time_series_split(df_cleaned2)

    # Genetic Algorithm optimization
    individu_fitness_min, _, _ = algoritma_genetika6(train, test, 
                                              input_data.population_size,
                                              input_data.generations,
                                              input_data.mutation_prob)
    alpha = to_decimal(individu_fitness_min["Alpha"])
    beta = to_decimal(individu_fitness_min["Beta"])
    gamma = to_decimal(individu_fitness_min["Gamma"])
    # Genetic Algorithm optimization
    individu_fitness_min2, _, _ = algoritma_genetika6(train2, test2, 
                                              input_data.population_size,
                                              input_data.generations,
                                              input_data.mutation_prob)
    alpha2 = to_decimal(individu_fitness_min2["Alpha"])
    beta2 = to_decimal(individu_fitness_min2["Beta"])
    gamma2 = to_decimal(individu_fitness_min2["Gamma"])

    # Holt-Winters Forecasting
    _, ramalan_periode, _ = holt(train, alpha, beta, gamma)
    _, ramalan_periode2, _ = holt(train2, alpha2, beta2, gamma2)
    

    # Calculate MAPE
    mape_score = MAPE(test, ramalan_periode)
    mape_score2 = MAPE(test2, ramalan_periode2)
    

    return PredictionResult(
        forecast=ramalan_periode,
        mape=mape_score,
        best_alpha=alpha,
        best_beta=beta,
        best_gamma=gamma,
        forecast2=ramalan_periode2,
        mape2=mape_score2,
        best_alpha2=alpha2,
        best_beta2=beta2,
        best_gamma2=gamma2,
    )