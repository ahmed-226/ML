document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('predictionForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = {
            Open: document.getElementById('Open').value,
            High: document.getElementById('High').value,
            Low: document.getElementById('Low').value,
            Volume: document.getElementById('Volume').value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            document.getElementById('predictionResult').innerText = `Prediction: ${result.prediction}`;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('predictionResult').innerText = 'Error making prediction';
        }
    });
});
