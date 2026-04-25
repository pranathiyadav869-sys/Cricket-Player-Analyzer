import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib
import os

# --- ASSUMES dataset_crickett.csv IS IN THE SAME DIRECTORY ---

def train_and_save_model(data_path="dataset_crickett.csv"):
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: '{data_path}' not found. Please ensure your dataset is in the project folder.")
        return

    feature_cols = [
        "matches played", "bat innings", "bat runs", "bat avg", "bat sr", "50s", "100s",
        "bowl innings", "overs", "wickets", "bowl avg", "econ", "bowl sr"
    ]

    # Handle missing 'bowl avg' if not in the dataset
    if "bowl avg" not in df.columns:
        df['bowl avg'] = 0.0
    
    X = df[feature_cols]
    y = df["role"]

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train-test split (for completeness)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )

    # Train Logistic Regression
    clf = LogisticRegression(max_iter=500, multi_class="multinomial", solver="lbfgs")
    print("Training Logistic Regression model...")
    clf.fit(X_train, y_train)

    # Save artifacts
    joblib.dump(clf, "role_classifier_logreg.pkl")
    joblib.dump(le, "role_label_encoder.pkl")
    joblib.dump(scaler, "role_scaler.pkl")

    print("\nModel, encoder, and scaler saved successfully.")

if __name__ == "__main__":
    train_and_save_model()