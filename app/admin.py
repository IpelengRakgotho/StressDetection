import streamlit as st
import pandas as pd
from app.utils import initialize_firebase  # Import the utility function
import firebase_admin
from firebase_admin import credentials, firestore, storage
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import io

initialize_firebase()

# Define the data cleaning function
def clean_dataset(dataset):
    st.write("Before cleaning:")
    st.dataframe(dataset.head())

    # 1. Handle Missing Values
    st.write("Handling missing values...")
    dataset = dataset.dropna()  # Remove rows with missing values

    # 2. Remove Duplicates
    st.write("Removing duplicates...")
    dataset = dataset.drop_duplicates()

    # 3. Correct Data Types
    if 'age' in dataset.columns:
        st.write("Converting 'age' to integers...")
        dataset['age'] = pd.to_numeric(dataset['age'], errors='coerce')  # Convert 'age' column to integers
    
    # 4. Handle Outliers
    if 'heart_rate' in dataset.columns:
        st.write("Capping 'heart_rate' values to realistic bounds...")
        dataset['heart_rate'] = dataset['heart_rate'].clip(lower=40, upper=180)

    # 5. Remove Irrelevant Features
    if 'id' in dataset.columns:
        st.write("Dropping irrelevant 'id' column...")
        dataset = dataset.drop(columns=['id'])

    st.write("After cleaning:")
    st.dataframe(dataset.head())
    
    return dataset
    
def train_model(cleaned_dataset1, cleaned_dataset2):
    # Ensure all datasets have the same columns
    all_columns = ['Gender', 'Age', 'heart_rate', 'hours_of_sleep', 'blood_oxygen', 'stress_level']

    # Add missing columns with default values
    for col in all_columns:
        if col not in cleaned_dataset1.columns:
            cleaned_dataset1[col] = 0
        if col not in cleaned_dataset2.columns:
            cleaned_dataset2[col] = 0

    # Combine the cleaned datasets
    combined_dataset = pd.concat([cleaned_dataset1, cleaned_dataset2], ignore_index=True)

    # Check columns before proceeding
    st.write("Columns in Combined Dataset:", combined_dataset.columns)

    # Select relevant features and target
    features = ['Gender', 'Age', 'heart_rate', 'hours_of_sleep', 'blood_oxygen']
    target = 'stress_level'

    # Check if all features and target columns exist
    missing_features = [col for col in features if col not in combined_dataset.columns]
    if missing_features:
        st.error(f"Missing columns in dataset: {missing_features}")
        return None
    
    if target not in combined_dataset.columns:
        st.error(f"Target column {target} not found in dataset!")
        return None

    # Encode categorical features (gender)
    le = LabelEncoder()
    combined_dataset['Gender'] = le.fit_transform(combined_dataset['Gender'].astype(str))

    # Define features (X) and target (y)
    X = combined_dataset[features]
    y = combined_dataset[target]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest Classifier
    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Model Accuracy: {accuracy:.2f}")

    return rf_model



  # Save datasets to Firebase Storage
def save_dataset_to_firebase(df, dataset_name):
  
    bucket = storage.bucket()
    blob = bucket.blob(f"datasets/{dataset_name}.csv")
    csv_data = df.to_csv(index=False)
    blob.upload_from_string(csv_data, content_type='text/csv')
    st.success(f"Dataset {dataset_name} saved to Firebase successfully!")

def admin_page():
    st.header("Admin Dashboard - Upload Datasets")
    
    # Upload Dataset 1
    st.subheader("Upload Dataset 1")
    dataset1_file = st.file_uploader("Upload Dataset 1 (CSV file)", type="csv", key='dataset1')
    cleaned_dataset1 = None
    if dataset1_file is not None:
        dataset1 = pd.read_csv(dataset1_file)
        cleaned_dataset1 = clean_dataset(dataset1)
        save_dataset_to_firebase(cleaned_dataset1, "dataset1")
    
    # Upload Dataset 2
    st.subheader("Upload Dataset 2")
    dataset2_file = st.file_uploader("Upload Dataset 2 (CSV file)", type="csv", key='dataset2')
    cleaned_dataset2 = None
    if dataset2_file is not None:
        dataset2 = pd.read_csv(dataset2_file)
        cleaned_dataset2 = clean_dataset(dataset2)
        save_dataset_to_firebase(cleaned_dataset2, "dataset2")
    
    # Train the model if both datasets are uploaded and cleaned
    if cleaned_dataset1 is not None and cleaned_dataset2 is not None:
        st.subheader("Train the Stress Detection Model")
        if st.button("Train Model"):
            model = train_model(cleaned_dataset1, cleaned_dataset2)
            if model:
                st.success("Model trained successfully")
                st.session_state['trained_model'] = model  # Save the model in the session for later use
