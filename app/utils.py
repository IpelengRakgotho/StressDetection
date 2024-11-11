import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:  # Ensure Firebase is initialized only once
        # Use a raw string or forward slashes in the file path
        cred = credentials.Certificate(r"app/stressguard-firebase-adminsdk-5rxfz-0582c96f1b.json")
        
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'stressguard.appspot.com'
        })
