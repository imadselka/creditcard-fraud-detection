import pandas as pd
import numpy as np
import joblib

# Load the trained model and scaler
model = joblib.load('best_fraud_detection_model.pkl')
scaler = joblib.load('scaler.pkl')

def predict_fraud(card_number, amount, time):
    # Extract features from card number
    card_features = [int(digit) for digit in card_number if digit.isdigit()]
    
    # Pad or truncate to 16 digits
    card_features = card_features[:16] + [0] * (16 - len(card_features))
    
    # Scale amount and time
    scaled_features = scaler.transform([[amount, time]])[0]
    
    # Combine all features
    features = card_features + list(scaled_features)
    
    # Pad with zeros to match the 30 features expected by the model
    features = features + [0] * (30 - len(features))
    
    # Reshape and predict
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    probability = model.predict_proba(features)[0][1]
    
    return bool(prediction[0]), probability

# Example usage
card_number = "4532015112830366"  # Example card number
amount = 100.0  # Example transaction amount
time = 43200  # Example time (12:00 PM in seconds since midnight)

is_fraudulent, fraud_probability = predict_fraud(card_number, amount, time)
print(f"Is fraudulent: {is_fraudulent}")
print(f"Fraud probability: {fraud_probability:.4f}")