import React from 'react';
import Plot from 'react-plotly.js';
import './SensorCharts.css';

function SensorCharts({ sensorHistory }) {
  if (sensorHistory.length === 0) {
    return (
      <div className="card">
        <h2>📊 Sensor Trends & Analytics</h2>
        <div className="empty-state">
          <p>No predictions yet. Submit sensor data to see visualizations.</p>
        </div>
      </div>
    );
  }

  // Prepare data for charts
  const timestamps = sensorHistory.map(item => 
    new Date(item.timestamp).toLocaleTimeString()
  );
  const temperatures = sensorHistory.map(item => item.temperature);
  const vibrations = sensorHistory.map(item => item.vibration);
  const pressures = sensorHistory.map(item => item.pressure);
  const failureProbabilities = sensorHistory.map(item => item.failure_probability * 100);

  // Chart layout configuration
  const layoutConfig = {
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
    font: { family: 'Arial, sans-serif', size: 12 },
    margin: { l: 60, r: 30, t: 30, b: 50 },
    xaxis: { title: 'Time' },
    hovermode: 'closest'
  };

  return (
    <div className="card">
      <h2>📊 Sensor Trends & Analytics</h2>
      <div className="charts-container">
        {/* Sensor Values Over Time */}
        <div className="chart-wrapper">
          <h3>Sensor Values Over Time</h3>
          <Plot
            data={[
              {
                x: timestamps,
                y: temperatures,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Temperature (°C)',
                line: { color: '#f44336', width: 2 },
                marker: { size: 6 }
              },
              {
                x: timestamps,
                y: vibrations,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Vibration (mm/s)',
                line: { color: '#2196f3', width: 2 },
                marker: { size: 6 },
                yaxis: 'y2'
              },
              {
                x: timestamps,
                y: pressures,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Pressure (PSI)',
                line: { color: '#4caf50', width: 2 },
                marker: { size: 6 },
                yaxis: 'y3'
              }
            ]}
            layout={{
              ...layoutConfig,
              title: 'Sensor Readings',
              yaxis: { title: 'Temperature (°C)', side: 'left' },
              yaxis2: { 
                title: 'Vibration (mm/s)', 
                overlaying: 'y', 
                side: 'right',
                position: 0.95
              },
              yaxis3: {
                title: 'Pressure (PSI)',
                overlaying: 'y',
                side: 'right',
                position: 0.98
              },
              height: 350
            }}
            config={{ responsive: true, displayModeBar: true }}
            style={{ width: '100%' }}
          />
        </div>

        {/* Failure Probability Over Time */}
        <div className="chart-wrapper">
          <h3>Failure Probability Trend</h3>
          <Plot
            data={[
              {
                x: timestamps,
                y: failureProbabilities,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Failure Probability',
                fill: 'tozeroy',
                fillcolor: 'rgba(244, 67, 54, 0.2)',
                line: { color: '#f44336', width: 3 },
                marker: { size: 8 }
              },
              {
                x: timestamps,
                y: Array(timestamps.length).fill(30),
                type: 'scatter',
                mode: 'lines',
                name: 'Low Threshold',
                line: { color: '#4caf50', width: 2, dash: 'dash' },
                showlegend: true
              },
              {
                x: timestamps,
                y: Array(timestamps.length).fill(70),
                type: 'scatter',
                mode: 'lines',
                name: 'High Threshold',
                line: { color: '#f44336', width: 2, dash: 'dash' },
                showlegend: true
              }
            ]}
            layout={{
              ...layoutConfig,
              title: 'Failure Risk Over Time',
              yaxis: { 
                title: 'Failure Probability (%)',
                range: [0, 100]
              },
              height: 350,
              shapes: [
                {
                  type: 'rect',
                  xref: 'paper',
                  yref: 'y',
                  x0: 0,
                  y0: 0,
                  x1: 1,
                  y1: 30,
                  fillcolor: 'rgba(76, 175, 80, 0.1)',
                  line: { width: 0 }
                },
                {
                  type: 'rect',
                  xref: 'paper',
                  yref: 'y',
                  x0: 0,
                  y0: 30,
                  x1: 1,
                  y1: 70,
                  fillcolor: 'rgba(255, 152, 0, 0.1)',
                  line: { width: 0 }
                },
                {
                  type: 'rect',
                  xref: 'paper',
                  yref: 'y',
                  x0: 0,
                  y0: 70,
                  x1: 1,
                  y1: 100,
                  fillcolor: 'rgba(244, 67, 54, 0.1)',
                  line: { width: 0 }
                }
              ]
            }}
            config={{ responsive: true, displayModeBar: true }}
            style={{ width: '100%' }}
          />
        </div>

        {/* Risk Level Distribution */}
        <div className="chart-wrapper">
          <h3>Risk Level Distribution</h3>
          <Plot
            data={[
              {
                x: sensorHistory.map(item => item.risk_level),
                type: 'histogram',
                marker: {
                  color: sensorHistory.map(item => {
                    switch (item.risk_level) {
                      case 'Low': return '#4caf50';
                      case 'Medium': return '#ff9800';
                      case 'High': return '#f44336';
                      default: return '#666';
                    }
                  })
                }
              }
            ]}
            layout={{
              ...layoutConfig,
              title: 'Risk Level Frequency',
              yaxis: { title: 'Count' },
              xaxis: { title: 'Risk Level' },
              height: 300
            }}
            config={{ responsive: true, displayModeBar: true }}
            style={{ width: '100%' }}
          />
        </div>
      </div>
    </div>
  );
}

export default SensorCharts;

