import datetime
import time
import smtplib

_email_list = [ ]
_offer_list = [ ]
_initial_offer_list =[]
_email_dont_send = [ ]

def sendEmailToOfferList( _o_list, _person_list, _matchingOList ):

  _email_list.clear()
  _email_list.clear()
  _initial_offer_list.clear()

  for _olist, olist in enumerate ( _o_list ):
    #ic( "sendEmilToOfferList: index=,", _olist, " balance= ", olist[ 'balance'], " timestamp= ", olist['timestamp'])
    for _mol, mol in enumerate( _matchingOList ):
      if ( olist['timestamp'] == mol ):
        _email_list.append( olist['offer_email'] )
        _offer_list.append( olist['balance'] )
        _initial_offer_list.append( olist['offer_amount'] )

  ic( "** Sending Offer thank you email ... ", _email_list, ",", _offer_list, ",", _initial_offer_list )
  #ic( 'sendEmail: olist[ts]=', olist['timestamp'], 'mol=', mol, 'email=', _o_list )

  _emailSender = 'claybogusky@sponsorhumanity.org'
  _mailPassword = 'Primrose#123#'

  # loop thru the email_list to find if the person wants email notifications or not... much to do bc I think people will want email.
 
  _emailTo = ""
 
  for _per, per in enumerate( _person_list ):
    for _eml, eml in enumerate( _email_list ):
      if ( eml == per['email'] ):
          #ic( "sendOfferEmail: ", per['send_email_on_match'] )
          _email_dont_send.append( per['send_email_on_match'])  
    
# for eds in _email_dont_send:
#    ic( "sendOfferEmail: eds = ", eds )

  x = datetime.datetime.now()

  for _eml, eml in enumerate( _email_list ):
    if ( _email_dont_send[ _eml ] == False ):
      #ic( "Person email setting is False!" )
      continue

    _emailTo = eml
    _emailDate = 'Date: ' + x.strftime("%m") + '/' + x.strftime("%d") + '/' + x.strftime("%G")
    _emailPerson = 'Dear ' + eml + ','
    _emailSentFrom = 'info@sponsorhumanity.org'

    _emailBody = "\n\n\n" + _emailPerson + "\n" + "\nCongratulations! Your offer of $" + str(_initial_offer_list[ _eml ]) + \
    " has been matched to purchase a grocery card for someone requesting support. " \
    "The remaining balance of your offer is $ " + str(_offer_list[ _eml ]) + \
    " The full amount of your offer is tax-deductible under the Internal Revenue Code, since Sponsor Humanity is a nonprofit organization" \
    "under Section 501(c)3 who provided no goods or services of value to you in consideration of your donation.  We recommend that you retain this email as a receipt.\n\n" \
    "Thank you for contributing to a shift in how we use and experience prosperity on the planet!\n\n" \
    "May it benefit both you and your match all the days of your life.\n\n" \
    "With gratitude,\n\n" \
    "Lindsay Samuels\n" \
    "Founder/Executive Director/President\n" \
    "Sponsor Humanity, Inc.\n" \
    "Federal EIN: 85-3426144\n" \
    "792 Preserve Terrace, Heathrow, FL 32746\n" \
    "info@sponsorhumanity.org\n" \
    "www.sponsorhumanity.org\n"

    _emailSubject = 'Sponsor Humanity thanks you!' 

    _emailText = """From: %s\nTo: %s\nSubject: %s\n%s
    %s
      """ % (_emailSentFrom, _emailTo, _emailSubject, _emailDate, _emailBody )

    #ic ( _emailText )

    try:
      # This MS SMTP server & port work well 19 April 2020 for hotmail
      #server = smtplib.SMTP( 'smtp-mail.outlook.com', 465 )

        # 465 or 587 for go daddy
      server = smtplib.SMTP( 'smtpout.secureserver.net', 587 )
      
      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login( _emailSender, _mailPassword )
      server.sendmail(_emailSentFrom, _emailTo, _emailText)
      server.close()

      ic ( '*** Email sent successfully ...' )
    except:
      ic ( 'Error sending Email ...something went wrong...' )



