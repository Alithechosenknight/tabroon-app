import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
import toml
import os

# Path to your secrets.toml file
TOML_PATH = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")

# Load the TOML file
secrets = toml.load(TOML_PATH)
cred_dict = dict(secrets["FIREBASE_SERVICE_ACCOUNT"])

# No need to touch the private_key!

# Initialize Firebase App
cred = credentials.Certificate(cred_dict)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore DB and Auth
db = firestore.client()
auth = firebase_auth
