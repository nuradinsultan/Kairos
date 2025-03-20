# microservices/fintech_service/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Kairos Fintech Service")

class PaymentRequest(BaseModel):
    user_id: int
    amount: float
    method: str  # e.g., 'Telebirr', 'M-Pesa'

@app.post("/process_payment")
def process_payment(request: PaymentRequest):
    # Here you would integrate with the Telebirr or M-Pesa API.
    # For demo, we simulate a successful payment.
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
    return {"status": "success", "message": f"Processed {request.method} payment of {request.amount} ETB for user {request.user_id}"}
