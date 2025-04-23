def forecast_model(model, steps=12):
    """
    Lakukan prediksi ke depan berdasarkan model Holt-Winters.
    """
    forecast = model.forecast(steps)
    return forecast