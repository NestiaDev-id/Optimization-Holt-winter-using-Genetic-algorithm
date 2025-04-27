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
    print(f"File path: {file_path}")
    df = load_excel_data(file_path)

    # Clean data
    df_cleaned = clean_data(df)

    # Split
    train, test = time_series_split(df_cleaned)

    # Genetic Algorithm optimization
    individu_fitness_min, _, _ = algoritma_genetika6(train, test, 
                                              input_data.population_size,
                                              input_data.generations,
                                              input_data.mutation_prob)
    alpha = to_decimal(individu_fitness_min["Alpha"])
    beta = to_decimal(individu_fitness_min["Beta"])
    gamma = to_decimal(individu_fitness_min["Gamma"])

    # Holt-Winters Forecasting
    _, ramalan_periode, _ = holt(train, alpha, beta, gamma)
    

    # Calculate MAPE
    mape_score = MAPE(test, ramalan_periode)
    

    return PredictionResult(
        forecast=ramalan_periode,
        mape=mape_score,
        best_alpha=alpha,
        best_beta=beta,
        best_gamma=gamma,
    )
