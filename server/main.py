from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming request data
class TransactionData(BaseModel):
    card_number: str
    amount: float

# Load your trained model and scaler
model = joblib.load("best_fraud_detection_model.pkl")
scaler = joblib.load("scaler.pkl")

# Luhn algorithm to validate card number
def luhn_algorithm(card_number):
    digits = [int(d) for d in str(card_number) if d.isdigit()]
    checksum = 0
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10 == 0

@app.post("/predict/")
async def predict(transaction: TransactionData):
    card_number = transaction.card_number
    amount = transaction.amount

    # Validate card number using Luhn algorithm
    is_valid_card = luhn_algorithm(card_number)

    # Extract features from card number
    card_features = [int(digit) for digit in card_number if digit.isdigit()]
    
    # Pad or truncate to 16 digits
    card_features = card_features[:16] + [0] * (16 - len(card_features))
    
    # Scale amount (assuming the scaler was trained only on the 'Amount' feature)
    scaled_amount = scaler.transform([[amount]])[0][0]
    
    # Combine all features
    features = card_features + [scaled_amount]
    
    # Pad with zeros to match the 30 features expected by the model
    features = features + [0] * (30 - len(features))
    
    # Reshape and predict
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    probability = model.predict_proba(features)[0][1]

    return {
        "is_fraudulent": bool(prediction[0]) or not is_valid_card,
        "fraud_probability": float(probability),
        "is_valid_card": is_valid_card
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}