document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const resultSymbolSpan = document.getElementById('result-symbol');
    const chartDiv = document.getElementById('chart');
    const detailsDiv = document.getElementById('details');
  
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const symbol = document.getElementById('symbol').value.toUpperCase();
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
  
        // Show loading spinner
        loadingDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
  
        try {
            // Fetch predictions from backend
            const response = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `symbol=${encodeURIComponent(symbol)}&start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`
            });
            const data = await response.json();
  
            if (data.error) throw new Error(data.error);
  
            // Update UI with results
            resultSymbolSpan.textContent = data.symbol;
  
            // Render chart using Plotly.js
            const historicalTrace = {
                x: [...Array(data.historical.length).keys()],
                y: data.historical,
                type: 'scatter',
                mode: 'lines',
                name: 'Historical Prices',
                line: { color: '#3498db' }
            };
  
            const predictionTrace = {
                x: [...Array(data.historical.length + data.predictions.length).keys()].slice(data.historical.length),
                y: data.predictions,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Predicted Prices',
                line: { color: '#e74c3c' }
            };
  
            Plotly.newPlot(chartDiv, [historicalTrace, predictionTrace], {
                title: `${data.symbol} Stock Price Prediction`,
                xaxis: { title: 'Days' },
                yaxis: { title: 'Price' }
            });
  
            // Display additional stock details
            detailsDiv.innerHTML = `
              <li><strong>Open:</strong> ${data.details.open.slice(-5).join(', ')}</li>
              <li><strong>High:</strong> ${data.details.high.slice(-5).join(', ')}</li>
              <li><strong>Low:</strong> ${data.details.low.slice(-5).join(', ')}</li>
            `;
  
            resultDiv.classList.remove('hidden');
        } catch (err) {
            alert(`Error fetching predictions:\n${err.message}`);
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });
  });
  