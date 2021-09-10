import Settings

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestor

# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

#
# Main storage lists & Classes
#
_person_list = []
_offer_list = []
_requests_list = []
settings = Settings


#
# read SETTINGS
#
print( 'Getting settings...')
sdoc = db.collection('settings').document("SponsorHumanity").get()
# for doc in sdocs:
settings.max_amount =  sdoc.get("max_amount_per_person" )
settings.max_household =  sdoc.get("max_household_size" )
settings.max_number_vendors =  sdoc.get("max_number_vendors" ) 
print( 'Settings: max amount, household_size, num_vendors', 
        settings.max_amount, settings.max_household, settings.max_number_vendors )

# 
# Get all PERSON and store them in list
#
print( 'Getting persons...')
_person = db.collection('person').get()
entry = "Jeannie4@jeanne.com"
for doc in _person: 
    _person_list.append( doc.to_dict())
for person in _person_list:
    if person['email'] == entry:
        print( "found entry", person['house_size']) 

#
# Get $$ OFFERS in chronological order and store them in list
#
print( 'Getting offers ...')
requests = db.collection('offers').order_by('timestamp').get()
_donorEmail = ""
_timeStamp = 0
_dollarsOffered = 0
_totalBalance = 0
for request in requests:
    _donorEmail =  request.get("offer_email")  
    _timeStamp = request.get ("timestamp") 
    _dollarsOffered = request.get("offer_amount")
    _balance = request.get("balance")
    _reserved = request.get("reserved")
    _totalBalance += _balance

    print( 'OFFER timestamp:', _timeStamp, '$ offered:', _dollarsOffered, 
            ' Balance:', _balance, 'reserved', _reserved, 'email:', _donorEmail ) 
    for doc in _person: 
        _offer_list.append( doc.to_dict())
print( "total balance $", _totalBalance )

# Get REQUESTS for $$ in chronological and store them in list
print( 'Getting requests ...')

requests = db.collection('requests').order_by('timestamp').get()
_donorEmail = ""
_timeStamp = 0
_dollarsRequested = 0
_totalRequested = 0
for request in requests:
    _donorEmail =  request.get("requestor_email")  
    _timeStamp = request.get ("timestamp") 
    _dollarsRequested = request.get("amount")
    _status = request.get("status")
    if ( _status == "ACTIVE"):
        _totalRequested += _dollarsRequested
    print( 'REQUEST timestamp = ', _timeStamp, ',$ requested = ', _dollarsRequested, 
            'email = ', _donorEmail, 'Status =', _status  )            
    for doc in _person: 
        _requests_list.append( doc.to_dict())
print( "total requested $", _totalRequested )

'''
print( 'with OUT order by')
docs = db.collection('requests').get()
print(len(docs))
for doc in docs:
#    print(doc.to_dict())
    junk =  doc.get("donor_email")  
    i = doc.get ("timestamp" )
    print( 'email = ', junk, ', timestamp = ', i  )  

# Get all documents
docs = db.collection('persons').get()
print(len(docs))
for doc in docs:
    print(doc.to_dict())

# Query
# Equal
docs = db.collection('persons').where("age", "==", 52 ).get()
print(" # 52 yo =", len(docs) )
for doc in docs:
    print(doc.to_dict())

# Greater than
docs = db.collection('persons').where("age", ">", 22 ).get()
print(" # >22 yo =", len(docs) )
for doc in docs:
    print(doc.to_dict())

# Array contains
docs = db.collection('persons').where("socials", "array_contains", "facebook").get()
for doc in docs:
    print(doc.to_dict())

# In
docs = db.collection('persons').where("address", "in", ["Milan", "London"]).get()
for doc in docs:
    print(doc.to_dict())
'''