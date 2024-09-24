from fastapi import FastAPI, HTTPException
import pickle
import numpy as np
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from sklearn.preprocessing import StandardScaler
import joblib

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and scaler
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'best_fraud_detection_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'scaler.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

scaler = joblib.load(scaler_path)

class CreditCardData(BaseModel):
    card_number: str
    amount: float
    time: float  # Assuming time is in seconds since midnight

def is_valid_card_number(card_number: str) -> bool:
    card_number = card_number.replace(" ", "")  # Remove spaces
    if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
        return False
    
    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Double every second digit
            n *= 2
            if n > 9:  # If doubling results in a number greater than 9, subtract 9
                n -= 9
        total += n
    
    return total % 10 == 0

def extract_features(card_number: str, amount: float, time: float):
    # Extract features from card number
    card_features = [int(digit) for digit in card_number if digit.isdigit()]
    
    # Pad or truncate to 16 digits
    card_features = card_features[:16] + [0] * (16 - len(card_features))
    
    # Scale amount and time using the pre-fitted scaler
    scaled_features = scaler.transform([[amount, time]])[0]
    
    # Combine all features
    features = card_features + list(scaled_features)
    
    # Pad with zeros to match the 30 features expected by the model
    features = features + [0] * (30 - len(features))
    
    return np.array(features).reshape(1, -1)

@app.post("/predict/")
def predict(data: CreditCardData):
    if not is_valid_card_number(data.card_number):
        raise HTTPException(status_code=400, detail="Invalid credit card number format.")

    try:
        features = extract_features(data.card_number, data.amount, data.time)
        prediction = model.predict(features)
        probability = model.predict_proba(features)[0][1]  # Probability of fraud
        
        return {
            "prediction": int(prediction[0]),
            "fraud_probability": float(probability),
            "is_fraudulent": bool(prediction[0])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)