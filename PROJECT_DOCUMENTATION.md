# Predictive Maintenance Dashboard - Complete Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
7. [API Documentation](#api-documentation)
8. [ML Model Details](#ml-model-details)
9. [Frontend Components](#frontend-components)
10. [Troubleshooting](#troubleshooting)
11. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

**Predictive Maintenance Dashboard** is an end-to-end machine learning system that predicts equipment failure probability using sensor data. The system consists of:

- **ML Pipeline**: Preprocesses NASA Turbofan Engine data, trains Random Forest Classifier
- **REST API**: Django backend serving predictions
- **Web Dashboard**: React.js frontend with interactive visualizations

### Key Features

✅ Real-time failure prediction from sensor inputs  
✅ Interactive Plotly charts for data visualization  
✅ Support for NASA real-world dataset (Hugging Face)  
✅ Support for synthetic dataset (for testing)  
✅ Risk level classification (Low/Medium/High)  
✅ Model evaluation metrics (Recall, Precision, F1-score)  

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  ← User Interface
│  (Port 3000)    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  Django REST API │  ← Business Logic
│  (Port 8000)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ML Service     │  ← Model Inference
│  (joblib models) │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Trained Model   │  ← Random Forest
│  + Scaler        │
└─────────────────┘
```

### Data Flow

1. **Training Phase**:
   - Load NASA dataset from Hugging Face
   - Preprocess (RUL calculation, feature selection)
   - Train Random Forest Classifier
   - Save model, scaler, and feature names

2. **Inference Phase**:
   - User inputs sensor values via frontend
   - Frontend sends POST request to Django API
   - API loads model and makes prediction
   - Returns failure probability and risk level
   - Frontend displays results and updates charts

---

## 💻 Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **CORS**: django-cors-headers 4.3.1
- **ML**: scikit-learn >= 1.4.0
- **Data**: pandas, numpy, joblib
- **Visualization**: plotly

### Frontend
- **Framework**: React.js 18.2.0
- **HTTP Client**: axios
- **Charts**: react-plotly.js, plotly.js
- **Build Tool**: react-scripts

### ML & Data
- **Dataset**: Hugging Face `LucasThil/nasa_turbofan_degradation_FD001`
- **Preprocessing**: pandas, numpy
- **Model**: Random Forest Classifier
- **Serialization**: joblib

---

## 📁 Project Structure

```
Predictive Maintenance Dashboard/
│
├── backend/                          # Django REST API
│   ├── api/                         # API application
│   │   ├── __init__.py
│   │   ├── apps.py                  # App configuration
│   │   ├── ml_service.py            # ML model service (inference)
│   │   ├── serializers.py           # DRF serializers
│   │   ├── views.py                 # API endpoints
│   │   └── urls.py                  # URL routing
│   │
│   ├── predictive_maintenance/      # Django project
│   │   ├── __init__.py
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # Root URL config
│   │   ├── wsgi.py                  # WSGI config
│   │   └── asgi.py                  # ASGI config
│   │
│   ├── manage.py                    # Django management script
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment
│
├── frontend/                        # React.js dashboard
│   ├── public/
│   │   └── index.html               # HTML template
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionForm.js   # Input form component
│   │   │   ├── PredictionForm.css
│   │   │   ├── PredictionResult.js # Results display
│   │   │   ├── PredictionResult.css
│   │   │   ├── SensorCharts.js     # Plotly charts
│   │   │   └── SensorCharts.css
│   │   │
│   │   ├── App.js                   # Main app component
│   │   ├── App.css                  # App styles
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Global styles
│   │
│   ├── package.json                 # Node dependencies
│   └── node_modules/                # Installed packages
│
├── ml/                              # Machine Learning
│   ├── models/                      # Trained models
│   │   ├── random_forest_model.joblib
│   │   ├── scaler.joblib
│   │   └── feature_names.joblib
│   │
│   ├── preprocess_huggingface_nasa.py  # NASA data preprocessing
│   ├── train_model.py               # Model training script
│   └── requirements_ml.txt          # ML dependencies
│
├── data/                            # Datasets
│   ├── nasa_processed.csv           # Processed NASA data
│   └── sensor_data.csv              # Synthetic dataset
│
├── README.md                        # Main documentation
├── QUICK_START_HUGGINGFACE.md       # Quick start guide
├── INSTALLATION_FIX.md              # Python 3.13 fix guide
└── PROJECT_DOCUMENTATION.md         # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python**: 3.11, 3.12, or 3.13 (3.13 requires scikit-learn >= 1.4.0)
- **Node.js**: 14+ and npm
- **Internet**: For downloading Hugging Face dataset (first time)

### Step 1: Clone/Download Project

```bash
# Navigate to project directory
cd "Predictive Maintenance Dashboard"
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (creates database)
python manage.py migrate
```

**Note**: If you're using Python 3.13 and get scikit-learn errors, see `INSTALLATION_FIX.md`

### Step 3: Preprocess NASA Dataset

```bash
# From project root
# Install datasets library if not already installed
pip install datasets

# Run preprocessing script
python ml/preprocess_huggingface_nasa.py
```

**Expected Output**:
```
Dataset loaded successfully!
Train dataset: 20,631 examples
Valid dataset: 13,096 examples
Final dataset shape: (33727, 25)
Failure rate: ~15-20%
```

### Step 4: Train ML Model

```bash
# From project root
# Ensure DATASET_TYPE = 'nasa' in ml/train_model.py
python ml/train_model.py
```

**Expected Output**:
```
MODEL EVALUATION METRICS
==================================================
Recall:    0.XXXX
Precision: 0.XXXX
F1-Score:  0.XXXX
...
Model saved to: ml/models/random_forest_model.joblib
```

### Step 5: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

### Step 6: Start Backend Server

```bash
# In a new terminal, navigate to backend
cd backend
venv\Scripts\activate  # Activate venv

# Start Django server
python manage.py runserver
```

### Step 7: Access Dashboard

Open browser: `http://localhost:3000`

---

## 📖 Usage Guide

### Using the Dashboard

1. **Enter Sensor Values**:
   - For NASA dataset: Enter `setting_1`, `setting_2`, `setting_3` and sensor values (`s_2`, `s_3`, etc.)
   - For synthetic dataset: Enter `temperature`, `vibration`, `pressure`

2. **Click "Predict Failure"**:
   - Frontend sends data to API
   - Model makes prediction
   - Results displayed immediately

3. **View Results**:
   - **Failure Probability**: Percentage (0-100%)
   - **Risk Level**: Low (<30%), Medium (30-70%), High (>70%)
   - **Prediction**: Binary (0 = Normal, 1 = Failure)

4. **Interactive Charts**:
   - **Sensor Trends**: Time series of sensor values
   - **Failure Probability Trend**: Risk over time
   - **Risk Distribution**: Histogram of risk levels

### Example API Request (cURL)

```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "setting_1": 0.0,
    "setting_2": 0.0,
    "setting_3": 100.0,
    "s_2": 518.67,
    "s_3": 1583.0,
    "s_4": 1400.60
  }'
```

### Example Response

```json
{
  "failure_probability": 0.85,
  "risk_level": "High",
  "prediction": 1
}
```

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. POST `/api/predict/`

Predict equipment failure probability.

**Request Body** (NASA Dataset):
```json
{
  "setting_1": 0.0,
  "setting_2": 0.0,
  "setting_3": 100.0,
  "s_2": 518.67,
  "s_3": 1583.0,
  "s_4": 1400.60,
  "s_7": 554.36,
  "s_8": 2388.06,
  "s_9": 9046.19,
  "s_11": 1.3,
  "s_12": 47.47,
  "s_13": 521.66,
  "s_14": 2388.02,
  "s_15": 8138.62,
  "s_17": 8.4195,
  "s_20": 0.03,
  "s_21": 392
}
```

**Request Body** (Synthetic Dataset):
```json
{
  "temperature": 95.5,
  "vibration": 6.2,
  "pressure": 132.0
}
```

**Response** (200 OK):
```json
{
  "failure_probability": 0.85,
  "risk_level": "High",
  "prediction": 1
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Invalid input data",
  "details": {
    "setting_1": ["This field is required."]
  }
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "error": "Model not found",
  "details": "Model not found at ... Please train the model first."
}
```

#### 2. GET `/api/features/`

Get list of required features for current model.

**Response** (200 OK):
```json
{
  "features": [
    "setting_1",
    "setting_2",
    "setting_3",
    "s_2",
    "s_3",
    ...
  ]
}
```

---

## 🤖 ML Model Details

### Model Architecture

- **Algorithm**: Random Forest Classifier
- **Parameters**:
  - `n_estimators`: 100 trees
  - `max_depth`: 15 (for NASA), 10 (for synthetic)
  - `class_weight`: 'balanced' (handles imbalanced data)
  - `random_state`: 42 (reproducibility)

### Preprocessing Pipeline

1. **Data Loading**:
   - Hugging Face dataset → pandas DataFrame
   - Combines train + valid splits

2. **Feature Engineering**:
   - **Operational Settings**: `setting_1`, `setting_2`, `setting_3`
   - **Key Sensors**: `s_2`, `s_3`, `s_4`, `s_7`, `s_8`, `s_9`, `s_11`, `s_12`, `s_13`, `s_14`, `s_15`, `s_17`, `s_20`, `s_21`
   - **Rolling Statistics**: Mean and std for top 5 sensors (trend indicators)

3. **Label Creation**:
   - **RUL**: Remaining Useful Life (from dataset)
   - **Failure Label**: 1 if RUL <= 30 cycles, 0 otherwise

4. **Scaling**:
   - StandardScaler (mean=0, std=1)
   - Fitted on training data, applied to test data

### Model Evaluation

Metrics calculated on test set (20% holdout):
- **Recall**: True Positives / (True Positives + False Negatives)
- **Precision**: True Positives / (True Positives + False Positives)
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)

### Model Files

- `random_forest_model.joblib`: Trained model
- `scaler.joblib`: StandardScaler for feature scaling
- `feature_names.joblib`: List of feature names (for API compatibility)

---

## 🎨 Frontend Components

### 1. PredictionForm

**Location**: `frontend/src/components/PredictionForm.js`

**Features**:
- Auto-detects dataset type (synthetic vs NASA)
- Dynamic form fields based on dataset
- Input validation
- Error handling
- Loading states

**Props**:
- `onPrediction(data)`: Callback when prediction is made

### 2. PredictionResult

**Location**: `frontend/src/components/PredictionResult.js`

**Features**:
- Circular progress indicator
- Risk level badge (color-coded)
- Detailed metrics display
- Visual indicators (✅ ⚠️ 🚨)

**Props**:
- `data`: Prediction result object

### 3. SensorCharts

**Location**: `frontend/src/components/SensorCharts.js`

**Features**:
- **Sensor Trends Chart**: Multi-axis time series
- **Failure Probability Trend**: Area chart with thresholds
- **Risk Distribution**: Histogram
- Interactive Plotly charts (zoom, pan, hover)

**Props**:
- `sensorHistory`: Array of prediction history

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'rest_framework'`
```bash
# Solution: Install dependencies
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: `Model not found` error
```bash
# Solution: Train the model first
python ml/train_model.py
```

**Problem**: CORS errors in browser
```bash
# Solution: Check CORS_ALLOWED_ORIGINS in settings.py
# Should include: "http://localhost:3000"
```

### Frontend Issues

**Problem**: `Cannot connect to API`
```bash
# Solution: Ensure backend is running on port 8000
cd backend
python manage.py runserver
```

**Problem**: `npm install` fails
```bash
# Solution: Clear cache and retry
npm cache clean --force
npm install
```

### ML Issues

**Problem**: `FileNotFoundError: nasa_processed.csv`
```bash
# Solution: Run preprocessing first
python ml/preprocess_huggingface_nasa.py
```

**Problem**: `scikit-learn` compilation errors (Python 3.13)
```bash
# Solution: See INSTALLATION_FIX.md
# Update requirements.txt to use scikit-learn >= 1.4.0
```

**Problem**: Poor model performance
```bash
# Solutions:
# 1. Adjust FAILURE_THRESHOLD in preprocess script
# 2. Increase n_estimators in train_model.py
# 3. Try different max_depth values
```

---

## 🚀 Future Enhancements

### Potential Improvements

1. **Model Improvements**:
   - Hyperparameter tuning (GridSearchCV)
   - Feature importance visualization
   - Model versioning
   - A/B testing different models

2. **API Enhancements**:
   - Authentication/Authorization
   - Rate limiting
   - Request logging
   - Batch predictions
   - Model retraining endpoint

3. **Frontend Enhancements**:
   - Real-time data streaming
   - Historical data storage
   - Export predictions to CSV
   - User authentication
   - Multiple equipment monitoring

4. **Infrastructure**:
   - Docker containerization
   - CI/CD pipeline
   - Cloud deployment (AWS, Azure, GCP)
   - Database integration (PostgreSQL)
   - Redis caching

5. **Advanced Features**:
   - Time series forecasting
   - Anomaly detection
   - Maintenance scheduling recommendations
   - Cost-benefit analysis
   - Multi-equipment dashboard

---

## 📝 Code Quality & Best Practices

### Backend
- ✅ Separation of concerns (ML service separate from views)
- ✅ Proper serializers for validation
- ✅ Error handling and status codes
- ✅ Model caching for performance
- ✅ CORS configuration

### Frontend
- ✅ Component-based architecture
- ✅ State management
- ✅ Error boundaries
- ✅ Responsive design
- ✅ Loading states

### ML
- ✅ Reproducible training (random_state)
- ✅ Feature engineering pipeline
- ✅ Model evaluation metrics
- ✅ Model persistence (joblib)

---

## 📚 Additional Resources

- **NASA Dataset**: https://huggingface.co/datasets/LucasThil/nasa_turbofan_degradation_FD001
- **Django REST Framework**: https://www.django-rest-framework.org/
- **React Documentation**: https://react.dev/
- **Plotly.js**: https://plotly.com/javascript/
- **Scikit-learn**: https://scikit-learn.org/

---

## 📄 License

This project is for educational purposes. The NASA Turbofan Engine Degradation Dataset is publicly available for research.

---

## 👥 Credits

- **Dataset**: NASA Prognostics Data Repository
- **Hugging Face**: Dataset hosting and preprocessing
- **Tech Stack**: Django, React, Scikit-learn communities

---

**Last Updated**: 2024
**Version**: 1.0.0

