import pandas as pd
import numpy as np
import streamlit as st
import cloudpickle
# from sklearn.preprocessing import OneHotEncoder

# Load the pre-trained pipeline
with open('poly_regression_pipeline.pkl', 'rb') as f:
    pipeline = cloudpickle.load(f)

# Define a function to make predictions
def predict(input_data):
    
    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data], columns=[ 
        'Usage_kWh',
        'Lagging_Current_Reactive.Power_kVarh',
        'Leading_Current_Reactive_Power_kVarh',
        'Lagging_Current_Power_Factor',
        'Leading_Current_Power_Factor',
        'NSM',
        'Day_sin',  # Ensure 'Day_sin' is present
        'Day_cos',  # Ensure 'Day_cos' is present
        'WeekStatus',
        'Load_Type'
    ])

    # Ensure correct data types (e.g., float for numeric columns, string for categorical columns)
    input_df['Usage_kWh'] = input_df['Usage_kWh'].astype(float)
    input_df['Lagging_Current_Reactive.Power_kVarh'] = input_df['Lagging_Current_Reactive.Power_kVarh'].astype(float)
    input_df['Leading_Current_Reactive_Power_kVarh'] = input_df['Leading_Current_Reactive_Power_kVarh'].astype(float)
    input_df['Lagging_Current_Power_Factor'] = input_df['Lagging_Current_Power_Factor'].astype(float)
    input_df['Leading_Current_Power_Factor'] = input_df['Leading_Current_Power_Factor'].astype(float)
    
    # Ensure NSM is treated as an integer
    input_df['NSM'] = input_df['NSM'].astype(int)

    input_df['Day_sin'] = input_df['Day_sin'].astype(float)
    input_df['Day_cos'] = input_df['Day_cos'].astype(float)

    # Handle missing values if there are any - This block is redundant as the user provides inputs
    input_df.fillna(0, inplace=True)

    # Handle unseen categories by checking if the input matches expected values
    week_status_map = {'Weekday': 0, 'Weekend': 1}
    load_type_map = {'Light': 0, 'Medium': 1, 'Heavy': 2}

    # Ensure that the week_status and load_type values are valid
    if input_df['WeekStatus'].iloc[0] not in week_status_map:
        raise ValueError(f"Invalid 'WeekStatus' value: {input_df['WeekStatus'].iloc[0]}")
    if input_df['Load_Type'].iloc[0] not in load_type_map:
        raise ValueError(f"Invalid 'Load_Type' value: {input_df['Load_Type'].iloc[0]}")

    input_df['WeekStatus'] = input_df['WeekStatus'].map(week_status_map)
    input_df['Load_Type'] = input_df['Load_Type'].map(load_type_map)

    # Use the pipeline to predict
    prediction = pipeline.predict(input_df)
    return prediction[0]

# Streamlit UI for input
st.title("CO2 Emission Prediction")

st.write(""" This app predicts CO2 emissions based on user inputs. """)

# Define the inputs for the user to fill in
usage_kwh = st.number_input('Enter Usage_kWh', min_value=0.0, step=1.0)
lagging_current_reactive_power_kvarh = st.number_input('Enter Lagging Current Reactive Power kVarh', min_value=0.0, step=1.0)
leading_current_reactive_power_kvarh = st.number_input('Enter Leading Current Reactive Power kVarh', min_value=0.0, step=1.0)
lagging_current_power_factor = st.number_input('Enter Lagging Current Power Factor', min_value=0.0, step=0.01)
leading_current_combined = st.number_input('Enter Leading Current Combined', min_value=0.0, step=1.0)
nsm = st.number_input('Enter NSM', min_value=0, step=1)  # Ensure NSM is entered as integer
day_sin = st.number_input('Enter Day Sin', min_value=-1.0, step=0.1)
day_cos = st.number_input('Enter Day Cos', min_value=-1.0, step=0.1)
week_status = st.selectbox('Select Week Status', ['Weekday', 'Weekend'])
load_type = st.selectbox('Select Load Type', ['Light', 'Medium', 'Heavy'])

# Collect all the inputs into a list
user_input = [
    usage_kwh, 
    lagging_current_reactive_power_kvarh, 
    leading_current_reactive_power_kvarh, 
    lagging_current_power_factor, 
    leading_current_combined, 
    nsm, 
    day_sin, 
    day_cos, 
    week_status, 
    load_type
]

# When the user clicks the "Predict" button
if st.button('Predict'):
    try:
        # Reshape input_data and pass it through the pipeline
        prediction = predict(user_input)
        st.write(f"Predicted CO2 Emission: {prediction:.2f} units")
    except ValueError as e:
        st.error(str(e))
