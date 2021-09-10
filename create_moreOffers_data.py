import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time

# Setup then load records to SH database collections

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

from datetime import datetime

# Delete all existing data
docs = db.collection('person').get() # Get all data
for doc in docs:
    key = doc.id
    db.collection('person').document(key).delete()

docs = db.collection('offers').get() # Get all data
for doc in docs:
    key = doc.id
    db.collection('offers').document(key).delete()

docs = db.collection('requests').get() # Get all data
for doc in docs:
    key = doc.id    
    db.collection('requests').document(key).delete()


# Using add to OFFERS collection
_email = 'cbogusky@hotmail.com' 
for i in range(10):
    #bucks = 10 * ( i % 10 + 1 )
    bucks = 100 + ( i * 10 )
    if ( _email == 'cbogusky@hotmail.com' ):
        _email = 'cbogusky@hotmail.com'
    elif ( _email == 'cbogusky@hotmail.com' ):
        _email = 'cbogusky@hotmail.com' 

    time.sleep( .01 )
    ts = int(time.time() * 1000)
    db.collection('offers').add({'offer_email': _email, 'phone':"999-999-9999", 
                                    'device_type': 'iPhone', 'serial_number': "1fyg2kkksa8",
                                    'offer_amount': bucks, 'balance': bucks, 
                                    'reserved': False, 'timestamp': ts })

sstatus = 'active'
#print("date and time:",date_time)

# Using add to REQUESTS collection
for i in range(10):
    bucks = 25 * ( i % 4 + 1 )
    sstatus = 'active'
    if ( _email == 'cbogusky@hotmail.com' ):
        _email = 'cbogusky@hotmail.com'
    elif ( _email == 'cbogusky@hotmail.com' ):
        _email = 'cbogusky@hotmail.com' 


    time.sleep( .01 )
    ts = int(time.time() * 1000)
    db.collection('requests').add({'requestor_email': _email, 'phone':"999-999-9999", 
                                    'device_type': 'iPhone', 'serial_number': "1fyg2kkksa8",
                                    'amount': bucks, 'status': "ACTIVE", 'timestamp': ts })

# add person
_uploaded = 'N'
for i in range(5): 
    emailAddr = 'lsamuels'
    emailAddr += str(i)
    emailAddr += '@yahoo.com' 
    #print( emailAddr )
    if ( i == 3 ):
        _uploaded = 'Y'
    else:
        _uploaded = 'N'
        
    db.collection('person').add ({ 'first_name':'Lindsay', 'last_name':'Samuels', 'email': emailAddr,
                                'phone':'999-999-9999', 'house_size':1, 'vendor_preference':'Walmart',
                                'number_of_vendors_per_request':1, 'geopoint':'', 'phone_type':'iphone',
                                'status': 'ACTIVE', 'send_email_on_match': False })
    emailAddr = ''

db.collection('person').add ({ 'first_name':'Clay', 'last_name':'Bogusky', 'email': 'cbogusky@hotmail.com',
                                'phone':'999-999-9999', 'house_size':1, 'vendor_preference':'Publix',
                                'number_of_vendors_per_request':1, 'geopoint':'', 'phone_type':'iphone',
                                'uploaded_receipt': 'Y', 'status': 'ACTIVE', 'send_email_on_match': False })

'''
# Add a new doc in collection 'persons' with ID 'HP'
db.collection('persons').document('HP').set(data)

# Merge new data with existing data for 'HP'
data = {'employed':True}
db.collection('persons').document('HP').set(data, merge=True)

# Using document() to get an auto generated ID with set()
data = {
    'name': 'Iron Man',
    'address': 'USA'
}
document_reference=db.collection('heroes').document()
document_reference.set(data)

# Adding subcollections
document_reference.collection('movies').add({'name':'Avengers'})
'''