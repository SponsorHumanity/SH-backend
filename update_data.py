import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time

# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

# Update data with unknown key
docs = db.collection('offers').get() # Get all data
for doc in docs:
    if doc.to_dict()["timestamp"] == 1618758965: # Check timestamp
        key = doc.id
        db.collection('offers').document(key).update({"balance": 0 } )

