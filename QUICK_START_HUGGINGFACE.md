# Quick Start Guide - Hugging Face NASA Dataset

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Install datasets library
pip install datasets

# Or install all ML requirements
pip install -r ml/requirements_ml.txt
```

### 2. Preprocess the Dataset

```bash
# From project root
python ml/preprocess_huggingface_nasa.py
```

This will:
- Download the dataset from Hugging Face (first time only, ~5-10 MB)
- Combine train and valid splits (33,727 total rows)
- Use the provided RUL to create failure labels
- Select 14 key sensors + 3 operational settings
- Add rolling statistics for trend analysis
- Save to `data/nasa_processed.csv`

**Expected output:**
```
Dataset loaded successfully!
Train dataset: 20,631 examples
Valid dataset: 13,096 examples
Final dataset shape: (33727, 25)
Failure rate: ~15-20%
```

### 3. Configure Training

In `ml/train_model.py`, ensure:
```python
DATASET_TYPE = 'nasa'
```

### 4. Train the Model

```bash
python ml/train_model.py
```

**Expected training time:** 1-3 minutes (depending on your machine)

### 5. Start Backend

```bash
cd backend
python manage.py runserver
```

### 6. Start Frontend

```bash
cd frontend
npm install  # First time only
npm start
```

### 7. Use the Dashboard

1. Open `http://localhost:3000`
2. The frontend will auto-detect NASA dataset
3. Enter sensor values:
   - **Operational Settings**: setting_1, setting_2, setting_3
   - **Key Sensors**: s_2, s_3, s_4, s_7, s_8, s_9, s_11, s_12, s_13, s_14, s_15, s_17, s_20, s_21
4. Click "Predict Failure"
5. View results and charts

## Dataset Details

- **Source**: Hugging Face - `LucasThil/nasa_turbofan_degradation_FD001`
- **Total Samples**: 33,727 (train + valid)
- **Features**: 
  - 3 operational settings (setting_1, setting_2, setting_3)
  - 14 key sensors (s_2 to s_21, selected)
  - 10 rolling statistics (mean, std for top 5 sensors)
- **Target**: Failure (1 if RUL <= 30 cycles, 0 otherwise)

## Troubleshooting

### Dataset Download Fails
- Check internet connection
- Ensure you have `datasets` installed: `pip install datasets`
- Try again - the dataset will be cached after first download

### Preprocessing Errors
- Make sure you're in the project root directory
- Check that `datasets` library is installed
- Verify the dataset name is correct: `LucasThil/nasa_turbofan_degradation_FD001`

### Model Training Issues
- Ensure preprocessing completed successfully
- Check that `data/nasa_processed.csv` exists
- Verify `DATASET_TYPE = 'nasa'` in `train_model.py`

### API Errors
- Make sure backend is running on port 8000
- Check that model files exist in `ml/models/`
- Verify feature names match between training and API

## Notes

- The dataset includes RUL (Remaining Useful Life) - we use it directly
- Failure threshold is 30 cycles (adjustable in preprocessing script)
- Rolling statistics are calculated per engine unit
- The model automatically handles missing rolling stats with defaults

