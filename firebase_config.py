import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Load credentials from secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"]))
    firebase_admin.initialize_app(cred)



# Initialize pyrebase for authentication
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# --- firebase-admin config (service account, keep secret) ---
# Try to load service account from environment variable, else fallback to default file
key_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_FILE", "sports-2f624-firebase-adminsdk-fbsvc-0e92d0d94c.json")
if not os.path.exists(key_path):
    raise FileNotFoundError(f"Firebase service account file not found: {key_path}")


db = firestore.client()
