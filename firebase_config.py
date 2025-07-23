import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# --- Pyrebase config (public, safe to include) ---
firebase_config = {
    "apiKey": "AIzaSyDFUhDzELGpZcZRCnK_pYAh7J4z5rgrGRU",
    "authDomain": "sports-2f624.firebaseapp.com",
    "databaseURL": "https://sports-2f624.firebaseio.com",
    "projectId": "sports-2f624",
    "storageBucket": "sports-2f624.appspot.com",
    "messagingSenderId": "427346095578",
    "appId": "1:427346095578:web:8bb4e91405b733b292a4e3"
}

# Initialize pyrebase for authentication
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- firebase-admin config (service account, keep secret) ---
# Try to load service account from environment variable, else fallback to default file
key_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_FILE", "sports-2f624-firebase-adminsdk-fbsvc-0e92d0d94c.json")
if not os.path.exists(key_path):
    raise FileNotFoundError(f"Firebase service account file not found: {key_path}")
cred = credentials.Certificate(key_path)

# Initialize firebase_admin if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "projectId": firebase_config["projectId"]
    })

db = firestore.client()
