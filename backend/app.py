

# Import necessary libraries
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
sales_forecasting_api = Flask("Product Store Sales Forecasting API")

# Load the trained machine learning model
model = joblib.load("superkart_prediction_model_v1_0.joblib")


# Define a route for the home page
@sales_forecasting_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/').
    """
    return "Welcome to the Product Store Sales Forecasting API!"


# Define an endpoint for single product sales prediction
@sales_forecasting_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects product and store details as JSON input.
    The derived features are calculated automatically.
    """

    # Get the JSON data from the request body
    product_data = request.get_json()

    # Create sample using user-provided features
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],

        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Type_Category': product_data['Product_Type_Category'],
    }

    # Convert the input into a DataFrame
    input_data = pd.DataFrame([sample])

    # ---------------------------------------------------------
    # Make prediction
    # ---------------------------------------------------------

    predicted_sales = model.predict(input_data)[0]

    # Convert prediction to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return prediction
    return jsonify({
        'Predicted Product Store Sales Total': predicted_sales
    })


# Define an endpoint for batch prediction
@sales_forecasting_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing the original input features.
    The derived features are calculated automatically.
    """

    # Get the uploaded CSV file
    file = request.files['file']

    # Read the CSV file
    input_data = pd.read_csv(file)

    input_data = input_data[numeric_features + categorical_features]

    # ---------------------------------------------------------
    # Make predictions
    # ---------------------------------------------------------

    predicted_sales = model.predict(input_data).tolist()

    # Round predictions
    predicted_sales = [
        round(float(sales), 2)
        for sales in predicted_sales
    ]

    return jsonify({
        'Predicted Product Store Sales Total': predicted_sales
    })


# Run the Flask application
if __name__ == '__main__':
    sales_forecasting_api.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )
