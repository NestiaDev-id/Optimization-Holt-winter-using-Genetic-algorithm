# app/services/model_service.py
from src.models import holt_winters, ga_optimizer

def predict_model(request):
    # TODO: Load model (kalau mau cache, tinggal pakai global var)
    # Dummy model prediksi: jumlah semua input
    prediction = sum(request.inputs)
    return {"prediction": prediction}
