import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PredictionForm.css';

const API_URL = 'http://localhost:8000/api/predict/';
const FEATURES_URL = 'http://localhost:8000/api/features/';

function PredictionForm({ onPrediction }) {
  const [datasetType, setDatasetType] = useState('synthetic'); // 'synthetic' or 'nasa'
  const [requiredFeatures, setRequiredFeatures] = useState([]);
  const [formData, setFormData] = useState({
    // Synthetic dataset
    temperature: '',
    vibration: '',
    pressure: '',
    // NASA dataset (Hugging Face format)
    setting_1: '',
    setting_2: '',
    setting_3: '',
    s_2: '', s_3: '', s_4: '', s_7: '', s_8: '', s_9: '',
    s_11: '', s_12: '', s_13: '', s_14: '', s_15: '', s_17: '', s_20: '', s_21: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch required features on mount
  useEffect(() => {
    fetchFeatures();
  }, []);

  const fetchFeatures = async () => {
    try {
      const response = await axios.get(FEATURES_URL);
      const features = response.data.features || [];
      setRequiredFeatures(features);
      
      // Detect dataset type based on features
      if (features.includes('setting_1') || features.includes('s_2') || 
          features.includes('op1') || features.includes('s2')) {
        setDatasetType('nasa');
      } else {
        setDatasetType('synthetic');
      }
    } catch (err) {
      console.log('Could not fetch features, using default');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Prepare data based on dataset type
      const payload = {};
      
      if (datasetType === 'synthetic') {
        payload.temperature = parseFloat(formData.temperature);
        payload.vibration = parseFloat(formData.vibration);
        payload.pressure = parseFloat(formData.pressure);
      } else {
        // NASA dataset (Hugging Face format) - include all provided values
        if (formData.setting_1) payload.setting_1 = parseFloat(formData.setting_1);
        if (formData.setting_2) payload.setting_2 = parseFloat(formData.setting_2);
        if (formData.setting_3) payload.setting_3 = parseFloat(formData.setting_3);
        
        // Support both formats (Hugging Face with underscore and old format)
        const nasaSensors = ['s_2', 's_3', 's_4', 's_7', 's_8', 's_9', 's_11', 's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21'];
        nasaSensors.forEach(sensor => {
          if (formData[sensor]) {
            payload[sensor] = parseFloat(formData[sensor]);
          }
        });
      }

      const response = await axios.post(API_URL, payload);

      onPrediction({
        input: formData,
        result: response.data,
        datasetType: datasetType
      });
    } catch (err) {
      setError(
        err.response?.data?.error || 
        err.response?.data?.details || 
        'Failed to get prediction. Make sure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>📊 Sensor Input</h2>
      <div className="dataset-info">
        <span className="dataset-badge">
          {datasetType === 'nasa' ? '🚀 NASA Dataset' : '🔧 Synthetic Dataset'}
        </span>
      </div>
      
      <form onSubmit={handleSubmit} className="prediction-form">
        {datasetType === 'synthetic' ? (
          <>
            <div className="form-group">
              <label htmlFor="temperature">
                Temperature (°C)
              </label>
              <input
                type="number"
                id="temperature"
                name="temperature"
                value={formData.temperature}
                onChange={handleChange}
                step="0.1"
                required
                placeholder="e.g., 95.5"
              />
            </div>

            <div className="form-group">
              <label htmlFor="vibration">
                Vibration (mm/s)
              </label>
              <input
                type="number"
                id="vibration"
                name="vibration"
                value={formData.vibration}
                onChange={handleChange}
                step="0.1"
                required
                placeholder="e.g., 6.2"
              />
            </div>

            <div className="form-group">
              <label htmlFor="pressure">
                Pressure (PSI)
              </label>
              <input
                type="number"
                id="pressure"
                name="pressure"
                value={formData.pressure}
                onChange={handleChange}
                step="0.1"
                required
                placeholder="e.g., 132.0"
              />
            </div>
          </>
        ) : (
          <>
            <div className="form-section">
              <h3>Operational Settings</h3>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="setting_1">Setting 1</label>
                  <input
                    type="number"
                    id="setting_1"
                    name="setting_1"
                    value={formData.setting_1}
                    onChange={handleChange}
                    step="0.1"
                    placeholder="e.g., 0.0"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="setting_2">Setting 2</label>
                  <input
                    type="number"
                    id="setting_2"
                    name="setting_2"
                    value={formData.setting_2}
                    onChange={handleChange}
                    step="0.1"
                    placeholder="e.g., 0.0"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="setting_3">Setting 3</label>
                  <input
                    type="number"
                    id="setting_3"
                    name="setting_3"
                    value={formData.setting_3}
                    onChange={handleChange}
                    step="0.1"
                    placeholder="e.g., 100.0"
                  />
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3>Key Sensors</h3>
              <div className="sensor-grid">
                {['s_2', 's_3', 's_4', 's_7', 's_8', 's_9', 's_11', 's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21'].map(sensor => (
                  <div className="form-group" key={sensor}>
                    <label htmlFor={sensor}>{sensor.replace('_', ' ').toUpperCase()}</label>
                    <input
                      type="number"
                      id={sensor}
                      name={sensor}
                      value={formData[sensor]}
                      onChange={handleChange}
                      step="0.01"
                      placeholder={`e.g., 500.0`}
                    />
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        <button 
          type="submit" 
          className="submit-btn"
          disabled={loading}
        >
          {loading ? 'Predicting...' : '🔮 Predict Failure'}
        </button>
      </form>
    </div>
  );
}

export default PredictionForm;
