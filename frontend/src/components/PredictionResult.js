import React from 'react';
import './PredictionResult.css';

function PredictionResult({ data }) {
  const { result } = data;
  const { failure_probability, risk_level, prediction } = result;

  const getRiskColor = (level) => {
    switch (level) {
      case 'Low':
        return '#4caf50';
      case 'Medium':
        return '#ff9800';
      case 'High':
        return '#f44336';
      default:
        return '#666';
    }
  };

  const getRiskIcon = (level) => {
    switch (level) {
      case 'Low':
        return '✅';
      case 'Medium':
        return '⚠️';
      case 'High':
        return '🚨';
      default:
        return '❓';
    }
  };

  return (
    <div className="card">
      <h2>📈 Prediction Result</h2>
      <div className="result-container">
        <div className="result-main">
          <div className="probability-circle">
            <div 
              className="circle-progress"
              style={{
                background: `conic-gradient(${getRiskColor(risk_level)} 0% ${failure_probability * 100}%, #e0e0e0 ${failure_probability * 100}% 100%)`
              }}
            >
              <div className="circle-inner">
                <span className="probability-value">
                  {(failure_probability * 100).toFixed(1)}%
                </span>
                <span className="probability-label">Failure Risk</span>
              </div>
            </div>
          </div>

          <div className="risk-badge" style={{ backgroundColor: getRiskColor(risk_level) }}>
            {getRiskIcon(risk_level)} {risk_level} Risk
          </div>
        </div>

        <div className="result-details">
          <div className="detail-item">
            <span className="detail-label">Prediction:</span>
            <span className="detail-value">
              {prediction === 1 ? '⚠️ Failure Likely' : '✅ Normal Operation'}
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Failure Probability:</span>
            <span className="detail-value">
              {(failure_probability * 100).toFixed(2)}%
            </span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Risk Level:</span>
            <span 
              className="detail-value"
              style={{ color: getRiskColor(risk_level), fontWeight: 'bold' }}
            >
              {risk_level}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PredictionResult;

