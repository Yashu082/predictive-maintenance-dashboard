# Predictive Maintenance Dashboard

A full-stack machine learning system that predicts equipment failure probability using sensor data from NASA's Turbofan Engine Degradation dataset. The system provides real-time risk assessment through a REST API and interactive web dashboard.
<img width="1866" height="970" alt="image" src="https://github.com/user-attachments/assets/ae39317f-7286-4c04-bd02-76ddf4d08776" />


## Problem Statement

Unplanned equipment failures in industrial settings lead to costly downtime, safety hazards, and production losses. Traditional maintenance approaches are either reactive (fix after failure) or time-based (schedule regardless of condition), both inefficient. Predictive maintenance uses sensor data and machine learning to forecast failures before they occur, enabling proactive intervention and optimized maintenance scheduling.

## What This System Does

- Trains a Random Forest classifier on NASA C-MAPSS turbofan engine sensor data
- Processes 27 features including operational settings, sensor readings, and rolling statistics
- Outputs failure probability (0-1) rather than binary predictions for nuanced risk assessment
- Serves predictions via Django REST API with automatic feature scaling
- Provides interactive dashboard with real-time predictions and trend visualization
- Classifies risk into Low (<30%), Medium (30-70%), and High (>70%) categories

## Architecture

```
┌─────────────────────┐
│  React Frontend     │  User inputs sensor values
│  (Port 3000)        │  Displays predictions & charts
└──────────┬──────────┘
           │ HTTP/REST
           ▼
┌─────────────────────┐
│  Django REST API    │  Validates input, handles requests
│  (Port 8000)        │  Returns JSON responses
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ML Service         │  Loads trained model & scaler
│  (Singleton)        │  Performs inference
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Random Forest      │  Predicts failure probability
│  Model (joblib)     │  from scaled sensor features
└─────────────────────┘
```

## Dataset

**NASA C-MAPSS FD001** (Commercial Modular Aero-Propulsion System Simulation) from Hugging Face. This dataset contains run-to-failure data from 100 turbofan engines with 21 sensor measurements and 3 operational settings recorded over multiple time cycles. The dataset is widely used in predictive maintenance research and provides realistic degradation patterns.

The preprocessing pipeline:
- Combines train and validation splits (33,727 total samples)
- Uses provided Remaining Useful Life (RUL) values
- Creates binary failure labels: failure = 1 if RUL ≤ 30 cycles, else 0
- Selects 14 key sensors (s_2, s_3, s_4, s_7, s_8, s_9, s_11 through s_15, s_17, s_20, s_21) based on predictive maintenance literature
- Adds rolling mean and standard deviation for top 5 sensors to capture degradation trends
- Results in 27 features total (3 settings + 14 sensors + 10 rolling statistics)

## Machine Learning Approach

**Model**: Random Forest Classifier with 100 trees, max depth of 15, and balanced class weights to handle imbalanced data (approximately 15-20% failure rate).

**Training Process**:
1. StandardScaler normalizes all features (mean=0, std=1)
2. 80/20 train-test split with stratification to preserve class distribution
3. Model trained on scaled training data
4. Evaluation metrics: Recall, Precision, F1-score on test set

**Output**: The model outputs failure probability (0.0 to 1.0) using `predict_proba()`, not just binary predictions. This allows for nuanced risk assessment where moderate sensor readings may show 25-30% failure probability, indicating early warning signs without triggering false alarms.

**Risk Classification**:
- **Low Risk** (< 30%): Normal operation, no immediate action needed
- **Medium Risk** (30-70%): Degradation detected, schedule inspection
- **High Risk** (≥ 70%): Imminent failure likely, immediate maintenance required

The conservative thresholding (30 cycles for failure label, 30% for low risk) reduces false positives, which is critical in industrial applications where unnecessary maintenance is costly.

## Dashboard Features

**Input Form**: Auto-detects dataset type and displays appropriate fields. For NASA dataset, accepts 3 operational settings and 14 key sensor values.

**Prediction Display**: Shows failure probability as circular progress indicator, risk level badge (color-coded), and binary prediction.

**Analytics Charts** (Plotly):
- Multi-axis time series of sensor values over prediction history
- Failure probability trend with Low/Medium/High threshold zones
- Risk level distribution histogram

All charts are interactive with zoom, pan, and hover tooltips.

## Tech Stack

**Backend**:
- Django 4.2.7 with Django REST Framework
- Scikit-learn ≥1.4.0 for Random Forest
- Pandas, NumPy for data processing
- Joblib for model serialization

**Frontend**:
- React 18.2.0 with functional components and hooks
- Axios for HTTP requests
- Plotly.js and react-plotly.js for interactive visualizations

**ML Pipeline**:
- Hugging Face `datasets` library for data loading
- StandardScaler for feature normalization
- Random Forest with balanced class weights

## Local Setup

### Prerequisites
- Python 3.11+ (3.13 requires scikit-learn ≥1.4.0)
- Node.js 14+ and npm
- Internet connection (first-time dataset download)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://localhost:8000`

### Preprocess Dataset & Train Model

```bash
# From project root
pip install datasets
python ml/preprocess_huggingface_nasa.py
python ml/train_model.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

## Explaining This Project in Interviews

This project demonstrates end-to-end ML system design: data preprocessing, model training, API development, and frontend integration. I chose NASA's C-MAPSS dataset because it's a real-world benchmark in predictive maintenance. The Random Forest model outputs probability scores rather than binary predictions, enabling risk stratification. The system is intentionally conservative—using a 30-cycle failure threshold and 30% risk threshold—to minimize false alarms, which is critical in industrial applications. The architecture separates concerns: ML logic in a service layer, REST API for integration, and React frontend for user interaction. This design allows the model to be retrained or swapped without changing API contracts.

## Future Improvements

- Hyperparameter tuning via GridSearchCV or Bayesian optimization
- Feature importance visualization to identify critical sensors
- Time-series forecasting to predict RUL directly (regression approach)
- Model versioning and A/B testing framework
- Batch prediction endpoint for processing multiple engines
- Database integration for historical prediction storage
- Authentication and rate limiting for production deployment
- Docker containerization for easier deployment

## Project Structure

```
├── backend/              # Django REST API
│   ├── api/              # API endpoints and ML service
│   └── requirements.txt
├── frontend/             # React dashboard
│   └── src/components/   # UI components
├── ml/                   # ML pipeline
│   ├── preprocess_huggingface_nasa.py
│   ├── train_model.py
│   └── models/           # Trained model artifacts
└── data/                 # Processed datasets
```

## Author

**Yaswanth Koppanathi**

Built as a portfolio project demonstrating full-stack ML engineering capabilities.

## Contact

- **GitHub**: [yaswanth-koppanathi-ai](https://github.com/yaswanth-koppanathi-ai)
- **Email**: yaswanthkoppanathi24@gmail.com
- **LinkedIn**: [yaswanth-koppanathi-ai](https://www.linkedin.com/in/yaswanth-koppanathi-ai/)

---

**If you found this project helpful, please give it a star!** 

## Project Stats

![GitHub last commit](https://img.shields.io/github/last-commit/yaswanth-koppanathi-ai/Predictive-Maintenance-Dashboard)
![GitHub issues](https://img.shields.io/github/issues/yaswanth-koppanathi-ai/Predictive-Maintenance-Dashboard)
![GitHub stars](https://img.shields.io/github/stars/yaswanth-koppanathi-ai/Predictive-Maintenance-Dashboard)
![GitHub forks](https://img.shields.io/github/forks/yaswanth-koppanathi-ai/Predictive-Maintenance-Dashboard)
