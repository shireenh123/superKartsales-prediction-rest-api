# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superKart_sales_predictor_api = Flask("Superkart Salese Predictor")

# Load the trained machine learning model
model = joblib.load("Sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@superKart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superKart_sales_predictor_api.post('/v1/superKart')
def predict_ssuper_kart_sales():
    """
    This function handles POST requests to the '/v1/superKart' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted sales as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': property_data['Product_Weight'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_Type': property_data['Product_Type'],
        'Product_MRP': property_data['Product_MRP'],
        'Store_Age_Years': property_data['Store_Establishment_Year'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type']
    }

    # Feature engineering 1
    input_data["Product_Id_char"] = property_data["Product_Id"].str[:2]
    input_data["Store_Age_Years"] = (
    2026 - property_data["Store_Establishment_Year"])

    perishable_products = [
    "Fruits and Vegetables",
    "Frozen Foods",
    "Dairy",
    "Meat"]

    input_data["Product_Type_Category"] = property_data["Product_Type"].apply(
    lambda x: "Perishables"
    if x in perishable_products
    else "Non Perishables")

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_log_sale = model.predict(input_data)[0]

    # Calculate actual price
   # predicted_sale = np.exp(predicted_log_sale)

    # Convert predicted_price to Python float
    predicted_sale = round(float(predicted_log_sale), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Sales)': predicted_sale})


# Define an endpoint for batch prediction (POST request)
@superKart_sales_predictor_api.post('/v1/superKartbatch')
def predict_rental_price_batch():
    """
    This function handles POST requests to the '/v1/superKartbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_log_sales = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_sales = [round(float(log_price), 2) for log_price in predicted_log_sales]

    # Create a dictionary of predictions with property IDs as keys
    property_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(property_ids, predicted_sales))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superKart_sales_predictor_api.run(debug=True)
