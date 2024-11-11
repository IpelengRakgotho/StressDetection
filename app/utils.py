import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st

# Function to initialize Firebase and return clients for Firestore and Storage
def initialize_firebase():
    if not firebase_admin._apps:  # Ensure Firebase is initialized only once
        # Load credentials from Streamlit secrets
        cred = credentials.Certificate({
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        
        # Initialize Firebase app with Firestore and Storage
        firebase_admin.initialize_app(cred, {
            'storageBucket': st.secrets["firebase"]["project_id"] + ".appspot.com"
        })

    # Initialize Firestore client and Storage bucket
    db = firestore.client()
    bucket = storage.bucket()
    
    return db, bucket

