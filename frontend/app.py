

import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://localhost:7860"

# Set the title of the Streamlit app
st.title("Product Store Sales Forecasting")


# ---------------------------------------------------------
# Online Prediction
# ---------------------------------------------------------

st.subheader("Online Prediction")

# Collect user input for product features

# Numeric Data

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66,
    step=0.01
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027,
    step=0.001,
    format="%.3f"
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08,
    step=0.01
)

# Categorical Data

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart",
        "Departmental Store"
    ]
)

product_id_char = st.selectbox(
    "Product ID Character",
    [
        "FD",
        "NC",
        "DR",
    ]
)

store_age_years = st.selectbox(
    "Store Age (Years)",
    [
        17, 27, 39, 28
    ]
)

product_type_category = st.selectbox(
    "Product Type Category",
    [
        "Non Perishables",
        "Perishables",
    ]
)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,

    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age_years,
    'Product_Type_Category': product_type_category
}])


# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/sales",
            json=input_data.to_dict(orient='records')[0]
        )

        if response.status_code == 200:

            prediction = response.json()[
                'Predicted Product Store Sales Total'
            ]

            st.success(
                f"Predicted Product Store Sales Total: {prediction}"
            )

        else:

            st.error(
                f"Prediction failed. Status code: {response.status_code}"
            )

            st.write(response.text)

    except requests.exceptions.RequestException:

        st.error(
            "Unable to connect to the prediction API."
        )


# ---------------------------------------------------------
# Batch Prediction
# ---------------------------------------------------------

st.subheader("Batch Prediction")

# Allow users to upload a CSV file
uploaded_file = st.file_uploader(
    "Upload CSV file for batch prediction",
    type=["csv"]
)


# Make batch prediction
if uploaded_file is not None:

    # Display uploaded data
    st.write("Uploaded Data")

    batch_data = pd.read_csv(uploaded_file)

    st.dataframe(batch_data)


    if st.button("Predict Batch", type="primary"):

        # Reset file position before sending it
        uploaded_file.seek(0)

        try:

            response = requests.post(
                f"{BACKEND_URL}/v1/salesbatch",
                files={"file": uploaded_file}
            )

            if response.status_code == 200:

                response_data = response.json()

                predictions = response_data[
                    'Predicted Product Store Sales Total'
                ]

                st.success(
                    "Batch predictions completed!"
                )

                # Add predictions to the uploaded data
                prediction_data = batch_data.copy()

                prediction_data[
                    'Predicted Product Store Sales Total'
                ] = predictions

                st.dataframe(prediction_data)

            else:

                st.error(
                    f"Batch prediction failed. "
                    f"Status code: {response.status_code}"
                )

                st.write(response.text)

        except requests.exceptions.RequestException:

            st.error(
                "Unable to connect to the prediction API."
            )
