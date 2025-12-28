"""
ML Service Module
Handles model loading and prediction logic
Supports both synthetic and NASA datasets
"""

import os
import joblib
import numpy as np
from pathlib import Path

# Paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / 'ml' / 'models' / 'random_forest_model.joblib'
SCALER_PATH = BASE_DIR / 'ml' / 'models' / 'scaler.joblib'
FEATURE_NAMES_PATH = BASE_DIR / 'ml' / 'models' / 'feature_names.joblib'

class MLService:
    """Service class for ML model operations"""
    
    _model = None
    _scaler = None
    _feature_names = None
    
    @classmethod
    def load_model(cls):
        """Load the trained model, scaler, and feature names"""
        if cls._model is None:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(
                    f"Model not found at {MODEL_PATH}. Please train the model first."
                )
            cls._model = joblib.load(MODEL_PATH)
        
        if cls._scaler is None:
            if not SCALER_PATH.exists():
                raise FileNotFoundError(
                    f"Scaler not found at {SCALER_PATH}. Please train the model first."
                )
            cls._scaler = joblib.load(SCALER_PATH)
        
        if cls._feature_names is None:
            if FEATURE_NAMES_PATH.exists():
                cls._feature_names = joblib.load(FEATURE_NAMES_PATH)
            else:
                # Fallback for old models (synthetic dataset)
                cls._feature_names = ['temperature', 'vibration', 'pressure']
        
        return cls._model, cls._scaler, cls._feature_names
    
    @classmethod
    def predict(cls, **sensor_data):
        """
        Predict failure probability from sensor data
        
        Args:
            **sensor_data: Dictionary of sensor values (flexible for different datasets)
        
        Returns:
            dict: Contains failure_probability, risk_level, and prediction
        """
        model, scaler, feature_names = cls.load_model()
        
        # Prepare input array in the correct feature order
        input_array = []
        for feature in feature_names:
            if feature in sensor_data:
                input_array.append(sensor_data[feature])
            else:
                # For rolling statistics, use default values if not provided
                if '_mean' in feature or '_std' in feature:
                    # Use median/default values for missing rolling stats
                    base_feature = feature.split('_')[0]
                    if base_feature in sensor_data:
                        # Simple defaults: mean = sensor value, std = 0
                        if '_mean' in feature:
                            input_array.append(sensor_data.get(base_feature, 0))
                        else:  # _std
                            input_array.append(0.0)
                    else:
                        input_array.append(0.0)
                else:
                    raise ValueError(
                        f"Missing required feature: {feature}. "
                        f"Required features: {feature_names}"
                    )
        
        # Convert to numpy array
        sensor_data_array = np.array([input_array])
        
        # Scale input
        sensor_data_scaled = scaler.transform(sensor_data_array)
        
        # Predict
        prediction = model.predict(sensor_data_scaled)[0]
        failure_probability = model.predict_proba(sensor_data_scaled)[0][1]
        
        # Determine risk level
        if failure_probability < 0.3:
            risk_level = "Low"
        elif failure_probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            'failure_probability': float(failure_probability),
            'risk_level': risk_level,
            'prediction': int(prediction)
        }
    
    @classmethod
    def get_required_features(cls):
        """Get the list of required features for the current model"""
        _, _, feature_names = cls.load_model()
        return feature_names
