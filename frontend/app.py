import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
product_id = st.text_input("Product Id", "FD6114")
product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
allocated_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.10)
product_type = st.text_input("Product Type", "Snack Foods")
mrp = st.number_input("Product MRP", min_value=0.0, value=150.0)
#store_id = st.selectbox("Store Id", ["OUT001", "OUT002", "OUT003", "OUT004"])
establishment_year = st.number_input("Store Establishment Year", 1980, 2025, 2009)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
city_type = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox(
        "Store Type",
        ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"]
    )

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Id': product_id,
    'Product_Weight': product_weight,
    'Product Sugar Content': sugar,
    'Product Allocated Area': allocated_area,
    'Product_Type': product_type,
    'Product_MRP' : Product MRP.
    'Store_Establishment_Year"': establishment_year,
    'Store_Size': store_size,
    'Store_Location_City_Type': city_type,
    'Store_Type': store_type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/superKart", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales (in dollars)']
        st.success(f"Predicted Supererkart sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/superKartbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
