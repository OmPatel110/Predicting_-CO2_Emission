import streamlit as st
import pickle
import numpy as np

# Load the pre-trained pipeline
with open('poly_regression_pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Define a function to make predictions
def predict(input_data):
    # Use the pipeline to predict
    prediction = pipeline.predict(np.array(input_data).reshape(1, -1))
    return prediction[0]

# Streamlit UI for input
st.title("CO2 Emission Prediction")

st.write("""
    This app predicts CO2 emissions based on user inputs.
""")

# Define the inputs for the user to fill in
usage_kwh = st.number_input('Enter Usage_kWh', min_value=0.0, step=1.0)
lagging_current_reactive_power_kvarh = st.number_input('Enter Lagging Current Reactive Power kVarh', min_value=0.0, step=1.0)
leading_current_reactive_power_kvarh = st.number_input('Enter Leading Current Reactive Power kVarh', min_value=0.0, step=1.0)
lagging_current_power_factor = st.number_input('Enter Lagging Current Power Factor', min_value=0.0, step=0.01)
leading_current_power_factor = st.number_input('Enter Leading Current Power Factor', min_value=0.0, step=0.01)
leading_current_combined = st.number_input('Enter Leading Current Combined', min_value=0.0, step=1.0)
nsm = st.number_input('Enter NSM', min_value=0.0, step=1.0)
day_sin = st.number_input('Enter Day Sin', min_value=-1.0, step=0.1)
day_cos = st.number_input('Enter Day Cos', min_value=-1.0, step=0.1)
week_status = st.selectbox('Select Week Status', ['Weekday', 'Weekend'])
load_type = st.selectbox('Select Load Type', ['Light', 'Medium', 'Heavy'])

# Collect all the inputs into a list
user_input = [usage_kwh, lagging_current_reactive_power_kvarh, leading_current_reactive_power_kvarh, 
              lagging_current_power_factor, leading_current_power_factor, leading_current_combined, 
              nsm, day_sin, day_cos, week_status, load_type]

# Map the categorical inputs to appropriate values if needed
week_status_map = {'Weekday': 0, 'Weekend': 1}
load_type_map = {'Light': 0, 'Medium': 1, 'Heavy': 2}

# Update the categorical values in user input
user_input[-2] = week_status_map[user_input[-2]]
user_input[-1] = load_type_map[user_input[-1]]

# When the user clicks the "Predict" button
if st.button('Predict'):
    prediction = predict(user_input)
    st.write(f"Predicted CO2 Emission: {prediction:.2f} units")

