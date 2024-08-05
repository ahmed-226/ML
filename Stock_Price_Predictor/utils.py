import joblib
import numpy as np

def preprocess(Open, High, Low, Volume):
    test_data = np.array([[Open, High, Low, Volume]])  # Use double brackets to create a 2D array
    trained_model = joblib.load('stock_prediction_model.pkl')
    predictions = trained_model.predict(test_data)
    return predictions
