import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
import streamlit as st
import json

# Load Firebase credentials from Streamlit secrets
cred_dict = st.secrets["FIREBASE_SERVICE_ACCOUNT"]
cred = credentials.Certificate(cred_dict)

# Initialize Firebase App
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore DB and Auth
db = firestore.client()
auth = firebase_auth
