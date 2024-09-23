# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import pickle
import warnings

# Ignore warnings for cleaner output
warnings.filterwarnings('ignore')

# Step 1: Data Loading and Preprocessing
# --------------------------------------

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

# Step 2: Model Training and Automated Selection
# ----------------------------------------------

# Define models to train
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(),
    'XGBoost': XGBClassifier(eval_metric='logloss', use_label_encoder=False)
}

# Function to evaluate models using cross-validation
def evaluate_models(X_train, y_train, models, scoring='roc_auc'):
    results = {}
    for model_name, model in models.items():
        # Perform 5-fold cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring=scoring)
        results[model_name] = {
            'mean_score': np.mean(cv_scores),
            'std_score': np.std(cv_scores)
        }
        print(f"{model_name}: Mean {scoring} = {np.mean(cv_scores):.4f}, Std = {np.std(cv_scores):.4f}")
    return results

# Evaluate models and get cross-validation scores
results = evaluate_models(X_train_sm, y_train_sm, models)

# Function to select the best model based on the mean ROC-AUC score
def select_best_model(results):
    best_model_name = max(results, key=lambda x: results[x]['mean_score'])
    print(f"\nBest Model: {best_model_name} with a mean ROC-AUC score of {results[best_model_name]['mean_score']:.4f}")
    return models[best_model_name]

# Select the best model based on cross-validation
best_model = select_best_model(results)

# Step 3: Model Evaluation on Test Set
# ------------------------------------

# Train the best model on the full training set
best_model.fit(X_train_sm, y_train_sm)

# Predict on the test set
y_pred = best_model.predict(X_test)
y_pred_proba = best_model.predict_proba(X_test)[:, 1]

# Print classification report and ROC-AUC score
print("\nTest Set Performance:")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Step 4: Plot the ROC Curve
# --------------------------

# Plot the ROC curve for the best model
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')
plt.show()

# Step 5: Save the Best Model for Deployment
# ------------------------------------------

# Save the best model to a file
with open('best_fraud_detection_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

print("Best model saved as 'best_fraud_detection_model.pkl'")
