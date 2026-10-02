
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Product Store Sales Forecasting")

# ---------------------------------------------------------
# Online Prediction
# ---------------------------------------------------------

st.subheader("Online Prediction")

# Collect user input for product features
product_id = st.text_input(
    "Product ID",
    value="FD6114"
)

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66,
    step=0.01
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027,
    step=0.001,
    format="%.3f"
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08,
    step=0.01
)

store_id = st.selectbox(
    "Store ID",
    [
        "OUT001",
        "OUT002",
        "OUT003",
        "OUT004",
    ]
)

store_establishment_year = st.selectbox(
    "Store Establishment Year",
    [
        2009,
        1987,
        1999,
        1998,
    ]
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


# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Id': product_id,
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_Type': product_type,
    'Product_MRP': product_mrp,
    'Store_Id': store_id,
    'Store_Establishment_Year': store_establishment_year,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type
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

                predictions = response.json()

                st.success(
                    "Batch predictions completed!"
                )

                # Convert predictions into a DataFrame
                prediction_data = pd.DataFrame(
                    list(predictions.items()),
                    columns=[
                        "Product_Id",
                        "Predicted Product Store Sales Total"
                    ]
                )

                st.dataframe(prediction_data)

            else:

                st.error(
                    f"Batch prediction failed. "
                    f"Status code: {response.status_code}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Unable to connect to the prediction API."
            )
