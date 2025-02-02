import os
import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the service account JSON file
cred = credentials.Certificate('firebase-serviceAccount.json')

firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
})

# Initialize Firestore
db = firestore.client()

# Get bucket instance
bucket = storage.bucket()