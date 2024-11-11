import firebase_admin
from firebase_admin import credentials, firestore, storage

# Function to initialize Firebase and return clients for Firestore and Storage
def initialize_firebase():
    if not firebase_admin._apps:  # Ensure Firebase is initialized only once
        
        cred = credentials.Certificate('app\stressguard-firebase-adminsdk-5rxfz-4722c2db1b.json') 
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'stressguard.appspot.com'
        })

    # Initialize Firestore client and Storage bucket
    db = firestore.client()
    bucket = storage.bucket()
    
    return db, bucket
