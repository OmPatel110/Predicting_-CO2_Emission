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
st.title("Hourly-Based CO2 Emission Prediction")
st.subheader("Accurately forecast your steel production’s environmental impact on an hourly basis and explore actionable insights for sustainability.")

# Define the inputs for the user to fill in with larger ranges
usage_kwh = st.number_input(
    'Enter Usage_kWh', 
    min_value=0.0, 
    step=10.0, 
    help="Typical value is around 120 kWh for an hourly period."
)
lagging_current_reactive_power_kvarh = st.number_input(
    'Enter Lagging Current Reactive Power kVarh', 
    min_value=0.0, 
    step=1.0,
    help="Typical value is around 60 for an hourly period."
)
leading_current_reactive_power_kvarh = st.number_input(
    'Enter Leading Current Reactive Power kVarh', 
    min_value=0.0, 
    step=1.0,
    help="Typical value is around 16 for an hourly period."
)
lagging_current_power_factor = st.number_input(
    'Enter Lagging Current Power Factor', 
    min_value=0.0, 
    step=1.0,
    help="Typical value is around 80 for an hourly period."
)
nsm = st.number_input(
    'Enter NSM', 
    min_value=0, 
    step=1000, 
    help="Typical value is around 42,000 for an hourly period."
)

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
            
            # Since the original data was collected at 15-minute intervals, multiply by 4 to scale to an hourly basis
            prediction_hourly = prediction * 4  # Scale to hourly CO2 emission

            # Display the prediction result for an hourly basis
            st.write(f"Predicted CO2 Emission (hourly basis): {prediction_hourly:.2f} tons")
            
            # Tree plantation analogy with a range (15 kg to 30 kg of CO2 per tree per year)
            co2_per_tree_min = 0.015  # 15 kg of CO2 per tree per year
            co2_per_tree_max = 0.030  # 30 kg of CO2 per tree per year
            
            # Calculate the range of equivalent trees
            min_trees = prediction_hourly / co2_per_tree_max
            max_trees = prediction_hourly / co2_per_tree_min
            
            # Display the range of trees for the predicted CO2 emission
            st.write(f"🌳 To offset this CO2 emission, you'd need between {min_trees:.0f} and {max_trees:.0f} trees! on hourly basis")
            
            # Fun fact about tree benefits
            st.write("""
                🌍 Planting trees helps absorb CO2, improve air quality, and support biodiversity.
                🌱 On average, a mature tree can absorb between 15 to 30 kg of CO2 annually. 
                It's a simple and effective way to contribute to a cleaner, greener planet!
            """)

            # Additional comparison to everyday activities (driving or flying)
            st.write(f"🚗 Did you know? This CO2 emission is equivalent to driving a car for about {prediction_hourly * 888:.1f} kilometers!")
            st.write(f"✈️ Or flying for about {prediction_hourly * 160:.1f} kilometers in an airplane!")

        except ValueError as e:
            st.error(f"Prediction error: {str(e)}")



