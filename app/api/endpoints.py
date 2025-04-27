from fastapi import APIRouter, HTTPException
from app.services.model_service import predict_passenger
from app.models.data_model import PredictionInput, PredictionResult

router = APIRouter()

@router.post("/predict", response_model=PredictionResult)
def predict(input_data: PredictionInput):
    try:
        result = predict_passenger(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/healthcheck")
def health_check():
    return {"status": "ok"}