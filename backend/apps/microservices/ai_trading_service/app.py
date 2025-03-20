# microservices/ai_trading_service/app.py
from fastapi import FastAPI
import random

app = FastAPI(title="Kairos AI Trading Service")

@app.get("/predict_stock")
def predict_stock(symbol: str):
    # Dummy prediction: In a real implementation, this would use trained ML models.
    prediction = round(random.uniform(100, 200), 2)
    return {"symbol": symbol, "predicted_price": prediction}
