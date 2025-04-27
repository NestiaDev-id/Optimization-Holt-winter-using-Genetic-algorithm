# app/api/endpoints.py
from fastapi import APIRouter
from app.models.data_model import PredictRequest, PredictResponse
from app.services.model_service import predict_model

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    result = predict_model(request)
    return result
