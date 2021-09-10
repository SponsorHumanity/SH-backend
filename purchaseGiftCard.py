import logging
import time
import os
import subprocess

import processSH
import krogerautomation
import publixautomation

def purchaseGiftCard( person, offerTS, request, totalAmountRequested ):
    # offerTS = list of unique offer timestamps that compose totalAmountRequested
    _giftcardStatus = 0

    ic( "Purchasing gift card...")
    ic( 'person email:', request['requestor_email'], 'card preference:', person['vendor_preference'],
              'request amount= ', request['amount'], ' request timestamp=', request['timestamp'] )

    if ( person['vendor_preference'] == "Walmart" ):
            _giftcardStatus = buyWalmartCard( totalAmountRequested, request['requestor_email'] )
    elif ( person['vendor_preference'] == "Publix" ):
            _giftcardStatus = buyPublixCard( totalAmountRequested, request['requestor_email'] )
    elif ( person['vendor_preference'] == "Kroger" ):
            _giftcardStatus = buyKrogerCard( totalAmountRequested, request['requestor_email'] )
    elif ( person['vendor_preference'] == "WholeFoods" ):
            _giftcardStatus = buyWholeFoodsCard( totalAmountRequested, request['requestor_email'] )
    else:   
        ic( " No vendor card selected. Using Walmart...")
        _giftcardStatus = buyWalmartCard( totalAmountRequested, request['requestor_email'] )

    #
    #  After gift card is purchased, reduce the amount in the offer record.
    #
    processSH.updateOfferAndRequest( offerTS, request['timestamp'], totalAmountRequested )
    return ( 0 )

def buyWalmartCard( cardAmount, emailAddress):
    ic( 'Buying Walmart card ...', cardAmount, ' for ', emailAddress )
    return( 0 )

def buyPublixCard( cardAmount, emailAddress ):
    ic( 'Buying Publix card ...', cardAmount, ' for ', emailAddress )
    publixautomation.error_handles('10', emailAddress )
    return( 0 )

def buyKrogerCard( cardAmount, emailAddress ):
    ic( 'Buying Kroger card ...', cardAmount, ' for ', emailAddress )
    if ( krogerautomation.error_handles('10', emailAddress ) == 0 ):
        return( 0 )
    else:
        return( -1 )

def buyWholeFoodsCard( cardAmount, emailAddress ):
    ic( 'Buying WholeFoods card ...', cardAmount, ' for ', emailAddress )
    return( 0 )

