import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib
import warnings

warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('creditcard.csv')

# Feature scaling for 'Amount' and 'Time'
scaler = StandardScaler()
df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1,1))
df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1,1))

# Drop the original 'Amount' and 'Time' columns
df.drop(['Amount', 'Time'], axis=1, inplace=True)

# Split data into features (X) and target (y)
X = df.drop('Class', axis=1)
y = df['Class']

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Apply SMOTE to handle class imbalance
smote = SMOTE(sampling_strategy='minority', random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

# Define models to train
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(),
    'XGBoost': XGBClassifier(eval_metric='logloss', use_label_encoder=False)
}

# Evaluate models and get cross-validation scores
for name, model in models.items():
    cv_scores = cross_val_score(model, X_train_sm, y_train_sm, cv=5, scoring='roc_auc')
    print(f"{name}: Mean roc_auc = {np.mean(cv_scores):.4f}, Std = {np.std(cv_scores):.4f}")

# Select the best model (Random Forest in this case)
best_model = RandomForestClassifier()
best_model.fit(X_train_sm, y_train_sm)

# Predict on the test set
y_pred = best_model.predict(X_test)
y_pred_proba = best_model.predict_proba(X_test)[:, 1]

# Print classification report and ROC-AUC score
print("\nTest Set Performance:")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Save the best model and scaler
joblib.dump(best_model, 'best_fraud_detection_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Best model and scaler saved as 'best_fraud_detection_model.pkl' and 'scaler.pkl'.")