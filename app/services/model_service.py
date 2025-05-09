from src.models.evaluate import MAPE
from src.models.ga_optimizer import algoritma_genetika6, to_decimal
from src.models.holt_winters import holt
from src.data.load_data import load_excel_data
from src.data.clean_data import clean_data
from src.data.split_data import time_series_split
from app.models.data_model import PredictionInput, PredictionResult
import sys
import os
from pydantic import BaseModel

# sys.path.append(os.path.abspath('../src'))

# def predict_passenger(input_data: PredictionInput):
#     # Load data
#     base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) 
#     file_path = os.path.join(base_path, 'data', 'raw', 'dataset original.xlsx')
#     file_path2 = os.path.join(base_path, 'data', 'raw', 'dataset luar.xlsx')
#     print(f"File path: {file_path}")
#     df = load_excel_data(file_path)
#     df2 = load_excel_data(file_path2)

#     # Clean data
#     df_cleaned = clean_data(df)
#     df_cleaned2 = clean_data(df2)

#     # Split
#     train, test = time_series_split(df_cleaned)
#     train2, test2 = time_series_split(df_cleaned2)

#     # Genetic Algorithm optimization
#     individu_fitness_min, _, _ = algoritma_genetika6(train, test, 
#                                               input_data.population_size,
#                                               input_data.generations,
#                                               input_data.mutation_prob)
#     alpha = to_decimal(individu_fitness_min["Alpha"])
#     beta = to_decimal(individu_fitness_min["Beta"])
#     gamma = to_decimal(individu_fitness_min["Gamma"])
#     # Genetic Algorithm optimization
#     individu_fitness_min2, _, _ = algoritma_genetika6(train2, test2, 
#                                               input_data.population_size,
#                                               input_data.generations,
#                                               input_data.mutation_prob)
#     alpha2 = to_decimal(individu_fitness_min2["Alpha"])
#     beta2 = to_decimal(individu_fitness_min2["Beta"])
#     gamma2 = to_decimal(individu_fitness_min2["Gamma"])

#     # Holt-Winters Forecasting
#     _, ramalan_periode, _ = holt(train, alpha, beta, gamma)
#     _, ramalan_periode2, _ = holt(train2, alpha2, beta2, gamma2)
    

#     # Calculate MAPE
#     mape_score = MAPE(test, ramalan_periode)
#     mape_score = MAPE(test2, ramalan_periode2)
    

#     return PredictionResult(
#         forecast=ramalan_periode,
#         mape=mape_score,
#         best_alpha=alpha,
#         best_beta=beta,
#         best_gamma=gamma,
#     )
class PredictionResponse(BaseModel):
    dalam_negeri: PredictionResult
    luar_negeri: PredictionResult

def predict_passenger(input_data: PredictionInput) -> PredictionResponse:
    # Load data
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) 
    file_path = os.path.join(base_path, 'data', 'raw', 'dataset original.xlsx')
    file_path2 = os.path.join(base_path, 'data', 'raw', 'dataset luar.xlsx')

    df = load_excel_data(file_path)
    df2 = load_excel_data(file_path2)

    # Clean data
    df_cleaned = clean_data(df)
    df_cleaned2 = clean_data(df2)

    # Split data
    train, test = time_series_split(df_cleaned)
    train2, test2 = time_series_split(df_cleaned2)

    # === Dalam Negeri ===
    individu_dalam, _, _ = algoritma_genetika6(train, test, 
                                               input_data.population_size,
                                               input_data.generations,
                                               input_data.mutation_prob)
    alpha = to_decimal(individu_dalam["Alpha"])
    beta = to_decimal(individu_dalam["Beta"])
    gamma = to_decimal(individu_dalam["Gamma"])

    _, forecast_dalam, _ = holt(train, alpha, beta, gamma)
    mape_dalam = MAPE(test, forecast_dalam)

    result_dalam = PredictionResult(
        forecast=forecast_dalam,
        mape=mape_dalam,
        best_alpha=alpha,
        best_beta=beta,
        best_gamma=gamma,
    )

    # === Luar Negeri ===
    individu_luar, _, _ = algoritma_genetika6(train2, test2, 
                                              input_data.population_size,
                                              input_data.generations,
                                              input_data.mutation_prob)
    alpha2 = to_decimal(individu_luar["Alpha"])
    beta2 = to_decimal(individu_luar["Beta"])
    gamma2 = to_decimal(individu_luar["Gamma"])

    _, forecast_luar, _ = holt(train2, alpha2, beta2, gamma2)
    mape_luar = MAPE(test2, forecast_luar)

    result_luar = PredictionResult(
        forecast=forecast_luar,
        mape=mape_luar,
        best_alpha=alpha2,
        best_beta=beta2,
        best_gamma=gamma2,
    )

    return PredictionResponse(
        dalam_negeri=result_dalam,
        luar_negeri=result_luar
    )