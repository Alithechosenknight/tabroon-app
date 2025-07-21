import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
# --- Pyrebase config (public, safe to include) ---
firebase_config = {
    "apiKey": "AIzaSyDFUhDzELGpZcZRCnK_pYAh7J4z5rgrGRU",
    "authDomain": "sports-2f624.firebaseapp.com",
    "databaseURL": "https://sports-2f624.firebaseio.com",  # Make sure this is correct
    "projectId": "sports-2f624",
    "storageBucket": "sports-2f624.appspot.com",
    "messagingSenderId": "427346095578",
    "appId": "1:427346095578:web:8bb4e91405b733b292a4e3"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- firebase-admin config (service account, keep secret) ---
try:
    import streamlit as st
    service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(service_account_info)
except Exception:
    # Fallback for local dev: load from file if available
    key_path = os.environ.get(
        "FIREBASE_SERVICE_ACCOUNT_FILE",
        "sports-2f624-firebase-adminsdk-fbsvc-eb59154d17.json"
    )
    print("Using service account key file:", key_path)
    print("File exists:", os.path.exists(key_path))
    cred = credentials.Certificate(key_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "projectId": firebase_config["projectId"]
    })

db = firestore.client()
