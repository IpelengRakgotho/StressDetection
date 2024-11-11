import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
import json

# Function to initialize Firebase and return clients for Firestore and Storage
def initialize_firebase():
    if not firebase_admin._apps:  # Ensure Firebase is initialized only once
        # Load and parse credentials from Streamlit secrets
        firebase_creds = json.loads(st.secrets["firebase_credentials"])
        cred = credentials.Certificate(firebase_creds)
        
        # Initialize Firebase app with Firestore and Storage
        firebase_admin.initialize_app(cred, {
            'storageBucket': firebase_creds["project_id"] + ".appspot.com"
        })

    # Initialize Firestore client and Storage bucket
    db = firestore.client()
    bucket = storage.bucket()
    
    return db, bucket
