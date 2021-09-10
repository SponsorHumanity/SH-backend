import Settings
import purchaseGiftCard
import unique
import greedy
import sendOfferEmail

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from icecream import ic

import logging

# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#
# Main storage lists & Classes
#
#_unique_olist = []
_person_list = []
_offer_list = []
_requests_list = []
_balance_list = []
_offerSearchList = []

#_total_balance = 0

settings = Settings

#
#  load data to lists 
#
def loadSponsorHumanityDB():

    #
    # read SETTINGS
    #
    ic( 'Retrieving settings...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()
    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )
    ic( 'Settings: max amount, household_size', settings.max_amount, settings.max_household )

    # 
    # Get all PERSON and store them in list 
    # Uploaded_recept (Y or N) Y is an authorized value
    # Status: approved, pending (approved is an authorized value) 
    #
    ic( 'Retrieving persons...')
    _person = db.collection('person').get()
    # load only "qualified" persons.
    for person in _person: 
        _person_list.append( person.to_dict())
    ic( "Number persons in list =", len(_person_list))

    # Get REQUESTS for $$ in chronological and store them in list
    ic( 'Retrieving requests ...')
    requests = db.collection('requests').order_by('timestamp').get()
    _timeStamp = 0
    _dollarsRequested = 0
    for request in requests:
        _requestorEmail =  request.get("requestor_email")  
        _timeStamp = request.get ("timestamp") 
        _dollarsRequested = request.get("amount")
        #ic( 'REQUEST timestamp = ', _timeStamp, ',$ requested = ', _dollarsRequested, 'email = ', _requestorEmail  )            
        _processedRequest = request.get( 'status')
        if ( _processedRequest.upper() == 'ACTIVE' ): # don't include requests previously processed (marked as 'PROCESSED')
            _requests_list.append( request.to_dict())
            
    #  load up offers ...
    loadOffers()
 
#
#  match requests to offers 
# 
def processRequests( ):

    ic( '# of requests =', len( _requests_list))
    _matchingOfferList = []
    _total_dollar_requests_processed = 0

    for rindex, _aRequest in enumerate( _requests_list ):
        _matchingOfferList.clear() 
        _processedThisRequest = False  

        # find the person status for eligibility and number of people in the family and multiply the $$ request
        _person = findPersonForRequest( _aRequest )
        ic( "REQUEST =", _aRequest['timestamp'], 'amount=', _aRequest['amount'], ' for person: ', _person['email'])
        _aRequestAmount = _aRequest['amount'] * _person['house_size']
        ic( 'Request for $', _aRequestAmount, _person['house_size'], _person['status'] )
        if ( _aRequestAmount > _total_balance ):
            ic( "Not enough offer money!!!! Requesed amount of $", _aRequestAmount, "greater than total balance of $", _total_balance ) 
            continue

        loadOffers()
        for currentOffer in _offer_list:
            if ( (currentOffer['balance'] == _aRequestAmount) and (_aRequest['status'] == 'ACTIVE') ):
                ic( "Balance == _aSeachAmount ", currentOffer['balance'], _aRequestAmount )
                _matchingOfferList.append( currentOffer[ 'timestamp'])
                _buyGCstatus = purchaseGiftCard.purchaseGiftCard(  _person, _matchingOfferList,
                                                                   _requests_list[rindex], _aRequestAmount )
                _total_dollar_requests_processed += _aRequestAmount
                _processedThisRequest = True

        loadOffers()
        if ( _processedThisRequest == False ):
            for currentOffer in _offer_list:
                if ( (currentOffer['balance'] > _aRequestAmount) and (_aRequest['status'] == 'ACTIVE') ):
                    ic( "Balance > _aSeachAmount ", currentOffer['balance'], _aRequestAmount )
                    _matchingOfferList.append( currentOffer[ 'timestamp'])
                    _buyGCstatus = purchaseGiftCard.purchaseGiftCard(  _person, _matchingOfferList,
                                                                    _requests_list[rindex], _aRequestAmount )
                    _total_dollar_requests_processed += _aRequestAmount
                    _processedThisRequest = True
    
        #ic( "matching offer list len =", len(_matchingOfferList))
        loadOffers()
        if ( _processedThisRequest == False ):
            coinsUsed = [0]*(_aRequestAmount+1)
            coinCount = [0]*(_aRequestAmount+1)
            ic( "Generating coins ..",  _guol, 'balance list:', _balance_list )
            _status = greedy.dpMakeChange( _guol, _aRequestAmount, coinCount, coinsUsed )
            if ( _status == 0 ):
                ic( "Can't make change for ", _aRequestAmount, ' from this list of coins', _guol )
            else:
                # search in _offer_list for 'coins', store timestamp of those offers, 
                # pass array of offers to purchaseCard()
                # buy card
                # update Offer DB
                # update offer list w/call to loadOffers
                #ic("The offer list:", _guol )
                _offerSearchList = greedy.icCoins( coinsUsed, _aRequestAmount )
                ic( "Searching for these $$ offers", _offerSearchList )
                _matchingOfferList = findMatchingOffers( _offerSearchList )
                ic( '_matchingOfferList=', _matchingOfferList )
                if ( validMattchingOfferlist(_matchingOfferList) == True ):
                    _buyGCstatus = purchaseGiftCard.purchaseGiftCard(  _person, _matchingOfferList,
                                                                       _requests_list[rindex], _aRequestAmount )
                _total_dollar_requests_processed += _aRequestAmount
                _processedThisRequest = True

        if ( _processedThisRequest == True ): 
            sendOfferEmail.sendEmailToOfferList( _offer_list, _person_list, _matchingOfferList )

    ic( 'Total amount of $$ requested processed = ',  _total_dollar_requests_processed )

def findPersonForRequest( request ):

    for _aPerson in _person_list:
        if ( ( request['requestor_email'] == _aPerson['email'])
            and ( _aPerson['status'] == 'ACTIVE') ):
            _returnPerson = _aPerson
            break
    return( _returnPerson )

def loadOffers():
    #
    # Get $$ OFFERS in chronological order and store them in list
    #
    ic( 'loaOffers() retrieving offers ...')
    offers = db.collection('offers').order_by('timestamp').get()
    _donorEmail = ""
    _timeStamp = 0
    _dollarsOffered = 0
    global _guol
    _guol = []
    _offer_list.clear() 

    for offer in offers:
        _donorEmail =  offer.get( "offer_email" )  
        _timeStamp = offer.get ( "timestamp" ) 
        _dollarsOffered = offer.get( "offer_amount" )
        _balance = offer.get( "balance" )
        if ( _balance > 0 ):
            #ic( 'OFFER timestamp = ', _timeStamp, ',$ balance = ', _balance, 'email = ', _donorEmail  ) 
            _offer_list.append( offer.to_dict())
            
    ic( "# of offers =",len(_offer_list))

    # generate list of unique offers for 'loose change' 
    # https://runestone.academy/runestone/books/published/pythonds/Recursion/DynamicProgramming.html

    global _total_balance
    _total_balance = 0
    _balance_list.clear()
    for _olist in _offer_list:
        if ( _olist['balance'] > 0 ):
            if ( _olist['reserved'] == False ):
                _total_balance += _olist[ 'balance' ]
                _balance_list.append( _olist['balance'] )

    _guol = unique.getUnique ( _balance_list )
    ic( '_unique offer list:', _guol, ' total balance=$', _total_balance )
    #return ( _guol )


def findMatchingOffers( offerSearchList ):

    ic( 'offerSearchList', offerSearchList )
    _offerTimeStampList = [0]* (len(offerSearchList))

    for _a, a in enumerate( offerSearchList ):
        ts = findTimestap( a )
        _offerTimeStampList[ _a ] = ts

    #ic( '_offerTimeStampList=', _offerTimeStampList )
    return( _offerTimeStampList )

def findTimestap( dollar ):
    for  _o, o in enumerate( _offer_list):
        if ( (dollar == o['balance']) and (o['reserved'] == False )):
            o['reserved'] = True
            return( o['timestamp'])
    return( 0 )

def validMattchingOfferlist( matchingOfferList ):
    if 0 in matchingOfferList:
        return False
    
    return( True )


def updateOfferAndRequest( offerTSlist, requestTS, totalGiftCardAmount ):

    ic( 'Marking request as PROCESSED for request timestamp', requestTS )
    # upate record in the in-memory request to Processed (only one request)
    for _rindex, _rRequest in enumerate( _requests_list ):
        if ( _rRequest[ 'timestamp' ] == requestTS ):
            _rRequest[ 'status' ] = "PROCESSED"
            break

  # Update requests' status using timestamp field
    docs = db.collection('requests').get() # Get all data
    for doc in docs:
        if doc.to_dict()["timestamp"] == requestTS: # Check timestamp
            key = doc.id
            db.collection('requests').document(key).update({ "status": "PROCESSED" } )
            break

    updateOfferBalance( offerTSlist, totalGiftCardAmount )

def updateOfferBalance( offerTimestampList, totalGiftCardAmount ):
    newBalance = 0
   # Update balance in offer collection with unknown key in OFFERS collection
    docs = db.collection('offers').get() # Get all data
    for doc in docs:
        for _ots, ots in enumerate ( offerTimestampList ): 
            if doc.to_dict()["timestamp"] == offerTimestampList[_ots]: # Check timestamp
                key = doc.id
                newBalance += doc.to_dict()['balance']

    if ( newBalance == totalGiftCardAmount ):
        for doc in docs:
            for _ots, ots in enumerate ( offerTimestampList ): 
                if doc.to_dict()["timestamp"] == offerTimestampList[_ots]: # Check timestamp
                    key = doc.id
                    ic( 'Reducing the offer balance to Zero for offer timestamp ', offerTimestampList[_ots] )
                    db.collection('offers').document(key).update({ "balance": 0, "reserved": True } )
    if ( newBalance > totalGiftCardAmount ):
        ic( 'Reducing the offer balance to ', newBalance - totalGiftCardAmount, ' for offer timestamp ', offerTimestampList[_ots] )
        db.collection('offers').document(key).update({ "balance": newBalance - totalGiftCardAmount, "reserved": False } )                  
        
    # upate records in the in-memory offer list
    for _oindex, _aOffer in enumerate( _offer_list ):
        for _ots, ots in enumerate ( offerTimestampList ):  
            if ( _aOffer[ 'timestamp' ] == offerTimestampList[ _ots ] ):
                # ic(" updateOfferBalance: timestamp = ", _aOffer[ 'timestamp' ] )
                if ( newBalance == totalGiftCardAmount  ):
                    _aOffer[ 'balance'] = 0
                if ( newBalance > totalGiftCardAmount ):
                    _aOffer[ 'balance' ] = newBalance - totalGiftCardAmount
'''    for _olist in _offer_list:
        ic( "updateOfferBalance: balance= ", _olist['balance'] )  
'''  
    