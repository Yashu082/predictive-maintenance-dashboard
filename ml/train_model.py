"""
ML Training Script for Predictive Maintenance
Trains a Random Forest Classifier on sensor data
Supports both synthetic and NASA datasets
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import recall_score, precision_score, f1_score, classification_report
import joblib
import os
from pathlib import Path

# Get project root (parent of ml directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset configuration - Set to 'synthetic' or 'nasa'
DATASET_TYPE = 'nasa'  # Change to 'synthetic' to use original dataset

# Paths
if DATASET_TYPE == 'nasa':
    DATA_PATH = PROJECT_ROOT / 'data' / 'nasa_processed.csv'
else:
    DATA_PATH = PROJECT_ROOT / 'data' / 'sensor_data.csv'

MODEL_PATH = PROJECT_ROOT / 'ml' / 'models' / 'random_forest_model.joblib'
SCALER_PATH = PROJECT_ROOT / 'ml' / 'models' / 'scaler.joblib'
FEATURE_NAMES_PATH = PROJECT_ROOT / 'ml' / 'models' / 'feature_names.joblib'

def load_and_preprocess_data():
    """Load and preprocess sensor data"""
    print(f"Loading data from: {DATA_PATH}")
    
    if not DATA_PATH.exists():
        if DATASET_TYPE == 'nasa':
            raise FileNotFoundError(
                f"NASA processed data not found at {DATA_PATH}\n"
                "Please run: python ml/preprocess_nasa_data.py first"
            )
        else:
            raise FileNotFoundError(f"Data file not found at {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Handle missing values
    if df.isnull().sum().sum() > 0:
        # Fill missing values with median for numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if col != 'failure':
                df[col].fillna(df[col].median(), inplace=True)
    
    # Separate features and target
    feature_cols = [col for col in df.columns if col != 'failure']
    X = df[feature_cols].values
    y = df['failure'].values
    
    print(f"\nFeatures used: {len(feature_cols)}")
    print(f"Feature names: {feature_cols[:10]}{'...' if len(feature_cols) > 10 else ''}")
    
    return X, y, feature_cols

def train_model():
    """Train Random Forest Classifier"""
    # Load and preprocess data
    X, y, feature_cols = load_and_preprocess_data()
    
    # Check class balance
    print(f"\nClass distribution:")
    print(f"Normal (0): {(y == 0).sum()} ({(y == 0).mean():.2%})")
    print(f"Failure (1): {(y == 1).sum()} ({(y == 1).mean():.2%})")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("\nTraining Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,  # Increased for more complex NASA data
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Handle class imbalance
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = rf_model.predict(X_test_scaled)
    y_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1]
    
    # Evaluation metrics
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION METRICS")
    print("="*50)
    print(f"Recall:    {recall:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("="*50)
    
    # Save model, scaler, and feature names
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(rf_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(feature_cols, FEATURE_NAMES_PATH)  # Save feature order
    
    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Scaler saved to: {SCALER_PATH}")
    print(f"Feature names saved to: {FEATURE_NAMES_PATH}")
    
    return rf_model, scaler, feature_cols

if __name__ == '__main__':
    train_model()
