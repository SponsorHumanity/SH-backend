import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from icecream import ic

import time

# Setup with cert to SH firestore
# then add records to the collections

def time_format():
    return f'{datetime.now()}|> '

ic.configureOutput( prefix=time_format, includeContext=True )
#ic.configureOutput( prefix=time_format )


cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

from datetime import datetime

def message( _text ):
    print( _text )
    
# Delete all existing data
ic(  'Deleting existing records...' )
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
_email = 'claytest1927@gmail.com' 
_email = 'cbogusky@hotmail.com' 

for i in range(10):
    #bucks = 10 * ( i % 10 + 1 )
    bucks = 25
    time.sleep( .01 )
    ts = int(time.time() * 1000)
    if ( _email == 'cbogusky@hotmail.com' ):
        _email = 'claytest1927@gmail.com'
    elif ( _email == 'claytest1927@gmail.com' ):
        _email = 'cbogusky@hotmail.com' 
    db.collection('offers').add({'offer_email': _email, 'phone':"999-999-9999", 
                                    'device_type': 'iPhone', 'serial_number': "1fyg2kkksa8",
                                    'offer_amount': bucks, 'balance': bucks, 
                                    'reserved': False, 'timestamp': ts })

sstatus = 'active'
#print("date and time:",date_time)
        
# Using add to REQUESTS collection
for i in range(2):
    bucks = 75
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
        
    db.collection('person').add ({ 'first_name':'Lindsay', 'last_name':'Samuels', 'email': emailAddr,
                                'phone':'999-999-9999', 'house_size':1, 'vendor_preference':'Kroger',
                                'number_of_vendors_per_request':1, 'geopoint':'', 'phone_type':'iphone',
                                'status': 'ACTIVE', 'send_email_on_match': True })
    emailAddr = ''

db.collection('person').add ({ 'first_name':'Clay', 'last_name':'Bogusky', 'email': 'cbogusky@hotmail.com',
                                'phone':'999-999-9999', 'house_size':1, 'vendor_preference':'Kroger',
                                'number_of_vendors_per_request':1, 'geopoint':'', 'phone_type':'iphone',
                                'status': 'ACTIVE', 'send_email_on_match': True })

db.collection('person').add ({ 'first_name':'Clay', 'last_name':'Bo', 'email': 'claytest1927@gmail.com',
                                'phone':'999-999-9999', 'house_size':2, 'vendor_preference':'Kroger',
                                'number_of_vendors_per_request':1, 'geopoint':'', 'phone_type':'iphone',
                                'status': 'ACTIVE', 'send_email_on_match': True })

ic( 'Done!' ) 
