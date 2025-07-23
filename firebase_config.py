import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

# Export Firestore client
db = firestore.client()
