import streamlit as st
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from app.utils import initialize_firebase

# Initialize Firebase (make sure this is done only once in your application)
initialize_firebase()

def save_to_firebase(user_data, prediction):
    # Initialize Firestore
    db = firestore.client()
    
    # Define a unique document ID (e.g., timestamp or UUID)
    doc_id = str(int(pd.Timestamp.now().timestamp()))
    
    # Convert numpy types to native Python types
    data = {
        'Gender': int(user_data['Gender'][0]),
        'Age': int(user_data['Age'][0]),
        'heart_rate': int(user_data['heart_rate'][0]),
        'hours_of_sleep': float(user_data['hours_of_sleep'][0]),
        'blood_oxygen': int(user_data['blood_oxygen'][0]),
        'Predicted_Stress_Level': int(prediction[0]),  # Save numeric prediction for aggregation
        'timestamp': pd.Timestamp.now()  # Save the timestamp
    }
    
    # Save the data to Firestore
    db.collection('user_predictions').document(doc_id).set(data)

def map_stress_level_to_label(stress_level):
    if stress_level == 0:
        return "No Stress - Fully relaxed, no tension or concerns"
    elif 1 <= stress_level <= 2:
        return "Minimal Stress - Calm, with occasional minor stressors"
    elif 3 <= stress_level <= 4:
        return "Low Stress - Slightly stressed, but easily manageable"
    elif 5 <= stress_level <= 6:
        return "Moderate Stress - Noticeable stress, you’re coping, but you might feel tension"
    elif 7 <= stress_level <= 8:
        return "High Stress - You may feel overwhelmed"
    elif 9 <= stress_level <= 10:
        return "Extreme Stress"
    else:
        return "Unknown"

def plot_stress_evolution():
    # Initialize Firestore
    db = firestore.client()

    # Retrieve user's stress level data from Firestore
    user_predictions_ref = db.collection('user_predictions')
    user_data = user_predictions_ref.order_by('timestamp').stream()
    
    # Create a list to hold the data
    data_list = []
    
    for doc in user_data:
        doc_data = doc.to_dict()

        # Convert Firestore timestamp (DatetimeWithNanoseconds) to Python date
        timestamp = doc_data['timestamp']
        timestamp_date = datetime.fromtimestamp(timestamp.timestamp()).date()  # Convert to date only

        data_list.append({
            'date': timestamp_date,
            'Predicted_Stress_Level': doc_data['Predicted_Stress_Level']  # Numeric data for aggregation
        })
    
    # Convert list to DataFrame
    if data_list:
        df = pd.DataFrame(data_list)
        df.set_index('date', inplace=True)

        # Ensure 'Predicted_Stress_Level' is numeric
        df['Predicted_Stress_Level'] = pd.to_numeric(df['Predicted_Stress_Level'], errors='coerce')

        # Group by date and calculate the mean stress level for each date
        df_grouped = df.groupby(df.index).mean()

        # Create a line chart with the date as the x-axis
        st.line_chart(df_grouped['Predicted_Stress_Level'])
    else:
        st.warning("No data available to plot.")

def user_page():
    #st.header("Stress Detection")
    st.markdown("### *StressGuard*", unsafe_allow_html=True)


    # Get the trained model from session state
    model = st.session_state.get('trained_model', None)
    
    if model is None:
        st.warning("The model is not trained yet. Please ask the admin to upload data and train the model.")
        return
    
    # Input fields for smartwatch data
    Gender = st.selectbox("Gender", ["Male", "Female"])
    Age = st.number_input("Age", min_value=10, max_value=100, step=1)
    heart_rate = st.number_input("Heart Rate", min_value=0, max_value=180, step=1)

    # Define normal heart rate range based on age
    if Age < 18:
        normal_range = (70, 100)  # Example range for children/teens
    else:
        normal_range = (60, 100)  # Example range for adults

    # Check if heart rate is within normal range
    if heart_rate > 0:  # Only check if a heart rate is entered
        if normal_range[0] <= heart_rate <= normal_range[1]:
            st.success("Your heart rate is within the normal range.")
        else:
            st.warning("Your heart rate is high. Please consider consulting a healthcare provider.")

    hours_of_sleep = st.number_input("Hours of Sleep", min_value=0.0, max_value=12.0, step=0.1)
    blood_oxygen = st.number_input("Blood Oxygen", min_value=0, max_value=100, step=1)
      
    # Check if blood oxygen is within the normal range
    if blood_oxygen > 0:  # Only check if a blood oxygen level is entered
        if 95 <= blood_oxygen <= 100:
            st.success("Your blood oxygen level is within the normal range.")
        else:
            st.warning("Your blood oxygen level is low. Please consider consulting a healthcare provider.")
    
    # Predict stress when the user clicks the button
    if st.button("Predict Stress Level"):
        # Preprocess input
        gender_numeric = 1 if Gender == "Male" else 0
        user_input = pd.DataFrame({
            'Gender': [gender_numeric],
            'Age': [Age],
            'heart_rate': [heart_rate],
            'hours_of_sleep': [hours_of_sleep],
            'blood_oxygen': [blood_oxygen]
        })
        
        # Predict the stress level using the trained model
        stress_prediction = model.predict(user_input)
        stress_label = map_stress_level_to_label(stress_prediction[0])
        
        # Display the prediction as a descriptive label with bold and larger font
        st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Predicted Stress Level: {stress_label}</p>", unsafe_allow_html=True)
        
        # Save user data and numeric prediction to Firebase
        save_to_firebase(user_input, stress_prediction)
    
    # Plot stress level evolution over time
    st.subheader("Stress Level Evolution Over Time")
    plot_stress_evolution()
