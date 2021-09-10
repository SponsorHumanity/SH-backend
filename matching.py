'''
Sponsor Humanity "Matching" deamon
17 March 2021
Steps:

Main enrty point... 
read from the 'settings' collection
read the oldest requests for support (sorted by timesamp - oldest on top) where they are 'active' 

for each request, 
    if requested amount <= current balance
        * read the email address of the requestor and read corresponding person profile using email address
        * check if person is eligible for support, if not log a message to the transaction log and continue to next request
        * start transaction
            check person's prefered gift card
            check person's # of family members (multiply $$ requested by # family members???)
            purchase gift card 
            email gift card
            decrement balance
            increment # of requests processed
            log a message to local storage
        * end transaction
        * if transaction fails
            log message to transation log
            rollback transaction
log transaction with stats
exit
'''
import processSH
import logging  
import datetime

from icecream import ic

def time_format():
    return f'{datetime.now()}|> '

ic.configureOutput( prefix=time_format, includeContext=True )

print( '*************************************************************')
print( '**********************  Matching BEGIN **********************')
print( '*************************************************************')


processSH.loadSponsorHumanityDB()
#print( 'matching UOL:', _uol )
processSH.processRequests( )
print( '*************************************************************')
print( '**********************  Matching END ************************')
print( '*************************************************************')








