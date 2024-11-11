import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
import json

def initialize_firebase():
    if not firebase_admin._apps:  # Initialize Firebase only once
        # Parse the JSON from Streamlit secrets
        firebase_creds = json.loads(st.secrets["firebase_credentials"])
        cred = credentials.Certificate(firebase_creds)
        
        firebase_admin.initialize_app(cred, {
            'storageBucket': f"{firebase_creds['project_id']}.appspot.com"
        })
    
    # Initialize Firestore client and Storage bucket
    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket
