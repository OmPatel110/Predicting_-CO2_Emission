import pandas as pd
import streamlit as st
import cloudpickle

# Load the pre-trained pipeline
with open('poly_regression_pipeline.pkl', 'rb') as f:
    pipeline = cloudpickle.load(f)

# Define the function to make predictions
def predict(input_data):
    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data], columns=[
        'Usage_kWh',
        'Lagging_Current_Reactive.Power_kVarh',
        'Leading_Current_Reactive_Power_kVarh',
        'Lagging_Current_Power_Factor',
        'NSM',
    ])
    
    # Ensure correct data types for numeric columns
    numeric_cols = [
        'Usage_kWh', 
        'Lagging_Current_Reactive.Power_kVarh', 
        'Leading_Current_Reactive_Power_kVarh', 
        'Lagging_Current_Power_Factor', 
        'NSM'
    ]
    
    input_df[numeric_cols] = input_df[numeric_cols].astype(float)
    
    # Predict using the pipeline
    prediction = pipeline.predict(input_df)
    return prediction[0]

# Streamlit UI for input
st.title("CO2 Emission Prediction")

st.write("""This app predicts CO2 emissions based on user inputs.""")

# Define the inputs for the user to fill in
usage_kwh = st.number_input('Enter Usage_kWh', min_value=0.0, step=1.0)
lagging_current_reactive_power_kvarh = st.number_input('Enter Lagging Current Reactive Power kVarh', min_value=0.0, step=1.0)
leading_current_reactive_power_kvarh = st.number_input('Enter Leading Current Reactive Power kVarh', min_value=0.0, step=1.0)
lagging_current_power_factor = st.number_input('Enter Lagging Current Power Factor', min_value=0.0, step=0.01)
nsm = st.number_input('Enter NSM', min_value=0, step=1)  # Ensure NSM is entered as integer

# Collect all the inputs into a dictionary
user_input = {
    'Usage_kWh': usage_kwh, 
    'Lagging_Current_Reactive.Power_kVarh': lagging_current_reactive_power_kvarh, 
    'Leading_Current_Reactive_Power_kVarh': leading_current_reactive_power_kvarh, 
    'Lagging_Current_Power_Factor': lagging_current_power_factor, 
    'NSM': nsm
}

# When the user clicks the "Predict" button
if st.button('Predict'):
    if usage_kwh == 0 or nsm == 0:
        # Display a warning toast-like message
        st.warning("Please enter valid values for Usage_kWh and NSM. They cannot be zero!")
    else:
        try:
            # Make the prediction with the updated user input
            prediction = predict(user_input)
            st.write(f"Predicted CO2 Emission: {prediction:.2f} tons")
        except ValueError as e:
            st.error(f"Prediction error: {str(e)}")
