import React, { useState } from 'react';
import './App.css';
import PredictionForm from './components/PredictionForm';
import PredictionResult from './components/PredictionResult';
import SensorCharts from './components/SensorCharts';

function App() {
  const [predictionData, setPredictionData] = useState(null);
  const [sensorHistory, setSensorHistory] = useState([]);

  const handlePrediction = (data) => {
    setPredictionData(data);
    // Add to history for charts
    setSensorHistory(prev => [...prev, {
      timestamp: new Date().toISOString(),
      temperature: data.input.temperature,
      vibration: data.input.vibration,
      pressure: data.input.pressure,
      failure_probability: data.result.failure_probability,
      risk_level: data.result.risk_level
    }]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔧 Predictive Maintenance Dashboard</h1>
        <p>Monitor equipment health and predict failures using ML</p>
      </header>
      
      <main className="App-main">
        <div className="container">
          <div className="left-panel">
            <PredictionForm onPrediction={handlePrediction} />
            {predictionData && (
              <PredictionResult data={predictionData} />
            )}
          </div>
          
          <div className="right-panel">
            <SensorCharts sensorHistory={sensorHistory} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;

