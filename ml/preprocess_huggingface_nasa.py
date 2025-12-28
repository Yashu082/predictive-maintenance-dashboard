"""
NASA Turbofan Engine Degradation Dataset Preprocessing
For Hugging Face dataset: LucasThil/nasa_turbofan_degradation_FD001

This script loads the dataset from Hugging Face and preprocesses it
for our predictive maintenance model.

Dataset Structure:
- unit_number: Engine unit ID
- time_cycles: Time cycle
- setting_1, setting_2, setting_3: Operational settings
- s_1 to s_21: 21 sensor readings
- RUL: Remaining Useful Life (already provided!)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datasets import load_dataset

# Get project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Output path
OUTPUT_PATH = PROJECT_ROOT / 'data' / 'nasa_processed.csv'

# Failure threshold (RUL <= this many cycles indicates failure)
FAILURE_THRESHOLD = 30

def load_huggingface_dataset():
    """Load NASA dataset from Hugging Face"""
    print("Loading NASA dataset from Hugging Face...")
    print("Dataset: LucasThil/nasa_turbofan_degradation_FD001")
    
    try:
        ds = load_dataset("LucasThil/nasa_turbofan_degradation_FD001")
        print(f"Dataset loaded successfully!")
        print(f"Available splits: {list(ds.keys())}")
        
        # Show dataset info
        if 'train' in ds:
            print(f"\nTrain dataset:")
            print(f"  Number of examples: {len(ds['train'])}")
            print(f"  Features: {list(ds['train'].features.keys())[:5]}...")
        
        if 'valid' in ds:
            print(f"\nValid dataset:")
            print(f"  Number of examples: {len(ds['valid'])}")
        
        return ds
    except Exception as e:
        raise Exception(
            f"Failed to load dataset from Hugging Face: {e}\n"
            "Make sure you have installed: pip install datasets\n"
            "And that you have internet connection to download the dataset."
        )

def convert_to_dataframe(ds):
    """Convert Hugging Face dataset to pandas DataFrame"""
    print("\nConverting to pandas DataFrame...")
    
    # Combine train and valid splits for more data
    train_data = ds['train']
    valid_data = ds['valid'] if 'valid' in ds else None
    
    # Convert to pandas
    train_df = pd.DataFrame(train_data)
    
    if valid_data is not None:
        valid_df = pd.DataFrame(valid_data)
        # Combine both splits
        df = pd.concat([train_df, valid_df], ignore_index=True)
        print(f"Combined train and valid splits")
    else:
        df = train_df
    
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)[:10]}...")
    
    return df

def create_failure_labels(df):
    """
    Create failure labels from RUL
    
    The dataset already has RUL, so we just need to create failure labels
    """
    print("\nCreating failure labels from RUL...")
    
    # Create failure label: 1 if RUL <= threshold, 0 otherwise
    df['failure'] = (df['RUL'] <= FAILURE_THRESHOLD).astype(int)
    
    print(f"\nRUL Statistics:")
    print(f"  Min RUL: {df['RUL'].min()}")
    print(f"  Max RUL: {df['RUL'].max()}")
    print(f"  Mean RUL: {df['RUL'].mean():.2f}")
    print(f"  Median RUL: {df['RUL'].median():.2f}")
    
    print(f"\nFailure Distribution:")
    normal_count = (df['failure'] == 0).sum()
    failure_count = (df['failure'] == 1).sum()
    total = len(df)
    print(f"  Normal (0): {normal_count} ({normal_count/total:.2%})")
    print(f"  Failure (1): {failure_count} ({failure_count/total:.2%})")
    
    return df

def select_features(df):
    """
    Select and engineer features from NASA dataset
    
    Uses the actual column names from the Hugging Face dataset:
    - setting_1, setting_2, setting_3 (operational settings)
    - s_1 to s_21 (sensors)
    """
    print("\nSelecting and engineering features...")
    
    # Operational settings
    op_settings = ['setting_1', 'setting_2', 'setting_3']
    
    # Key sensors commonly used in predictive maintenance
    # Using sensors: s_2, s_3, s_4, s_7, s_8, s_9, s_11, s_12, s_13, s_14, s_15, s_17, s_20, s_21
    key_sensor_numbers = [2, 3, 4, 7, 8, 9, 11, 12, 13, 14, 15, 17, 20, 21]
    key_sensors = [f's_{i}' for i in key_sensor_numbers]
    
    print(f"Selected {len(key_sensors)} key sensors: {key_sensors[:5]}...")
    
    # Create feature dataframe
    features_df = df[['unit_number', 'time_cycles', 'failure']].copy()
    
    # Add operational settings
    for op in op_settings:
        if op in df.columns:
            features_df[op] = df[op]
            print(f"  Added: {op}")
    
    # Add key sensors
    for sensor in key_sensors:
        if sensor in df.columns:
            features_df[sensor] = df[sensor]
    
    print(f"  Added {len([s for s in key_sensors if s in df.columns])} sensors")
    
    # Add rolling statistics for top 5 sensors (trend indicators)
    top_sensors = key_sensors[:5]
    print(f"\nAdding rolling statistics for top 5 sensors...")
    
    for sensor in top_sensors:
        if sensor in df.columns:
            # Rolling mean (trend) - calculated per unit
            features_df[f'{sensor}_mean'] = df.groupby('unit_number')[sensor].transform(
                lambda x: x.expanding().mean()
            )
            # Rolling std (variability) - calculated per unit
            features_df[f'{sensor}_std'] = df.groupby('unit_number')[sensor].transform(
                lambda x: x.expanding().std().fillna(0)
            )
            print(f"  Added rolling stats for: {sensor}")
    
    return features_df

def preprocess_huggingface_dataset():
    """Main preprocessing function"""
    print("="*60)
    print("NASA Turbofan Engine Degradation Dataset Preprocessing")
    print("Source: Hugging Face - LucasThil/nasa_turbofan_degradation_FD001")
    print("="*60)
    
    # Load dataset from Hugging Face
    ds = load_huggingface_dataset()
    
    # Convert to DataFrame
    df = convert_to_dataframe(ds)
    
    # Create failure labels from RUL
    processed_df = create_failure_labels(df)
    
    # Select and engineer features
    features_df = select_features(processed_df)
    
    # Handle missing values
    print("\nHandling missing values...")
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns
    missing_count = 0
    for col in numeric_cols:
        if col not in ['unit_number', 'time_cycles', 'failure']:
            if features_df[col].isnull().sum() > 0:
                missing_count += features_df[col].isnull().sum()
                features_df[col].fillna(features_df[col].median(), inplace=True)
    
    if missing_count > 0:
        print(f"  Filled {missing_count} missing values")
    else:
        print("  No missing values found")
    
    # Remove unit and cycle columns (not needed for training)
    final_df = features_df.drop(['unit_number', 'time_cycles'], axis=1)
    
    # Save processed data
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(OUTPUT_PATH, index=False)
    
    print(f"\n{'='*60}")
    print(f"Preprocessing complete!")
    print(f"Processed data saved to: {OUTPUT_PATH}")
    print(f"Final dataset shape: {final_df.shape}")
    print(f"\nFeatures ({len(final_df.columns)-1}):")
    for i, col in enumerate(final_df.columns):
        if col != 'failure':
            print(f"  {i+1}. {col}")
    print(f"\nFailure rate: {final_df['failure'].mean():.2%}")
    print(f"{'='*60}")
    
    return final_df

if __name__ == '__main__':
    preprocess_huggingface_dataset()
