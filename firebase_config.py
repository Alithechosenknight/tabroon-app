import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

firebase_config = {
    "apiKey": "AIzaSyDFUhDzELGpZcZRCnK_pYAh7J4z5rgrGRU",
    "authDomain": "sports-2f624.firebaseapp.com",
    "databaseURL": "https://your-app.firebaseio.com",  # <--- Add this line
    "projectId": "sports-2f624",
    "storageBucket": "sports-2f624.firebasestorage.app",
    "messagingSenderId": "427346095578",
    "appId": "1:427346095578:web:8bb4e91405b733b292a4e3"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

cred = credentials.Certificate("C:\python\StreamLit\serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "projectId": firebase_config["projectId"]
    })

db = firestore.client()
