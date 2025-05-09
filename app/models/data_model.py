from pydantic import BaseModel
from typing import List

class DataPoint(BaseModel):
    month: str
    passengers: int

class PredictionInput(BaseModel):
    population_size: int
    generations: int
    mutation_prob: int

class PredictionResult(BaseModel):
    forecast: List[float]
    mape: float
    best_alpha: float
    best_beta: float
    best_gamma: float
