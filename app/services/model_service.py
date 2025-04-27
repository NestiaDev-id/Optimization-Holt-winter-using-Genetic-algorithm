# app/models/data_model.py
from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    inputs: List[float]  # Misalnya input model adalah list angka

class PredictResponse(BaseModel):
    prediction: float
