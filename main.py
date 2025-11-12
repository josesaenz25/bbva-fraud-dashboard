from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Transaccion(BaseModel):
    amount: float
    hour: int
    threshold: float

@app.post("/predict")
def predict(data: Transaccion):
    # Simulación de lógica con umbral
    score = (data.amount / 6000) + (data.hour / 24)
    fraude = 1 if score > data.threshold else 0
    return {"fraude": fraude}
