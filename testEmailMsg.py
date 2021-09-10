import datetime

x = datetime.datetime.now()

_emailTo = 'claybogusky@sponsorhumanity.org' 
_emailDate = 'Date: ' + x.strftime("%m") + '/' + x.strftime("%d") + '/' + x.strftime("%G")
#print( _emailDate )
_emailPerson = 'Dear ' + _emailTo + ","
_emailSentFrom = 'clay'

_emailBody =  _emailPerson + "\n" + "\n\nCongratulations! Your offer of $____ has been matched to purchase a grocery card for someone requesting support."\
"The full amount of your offer is tax-deductible under the Internal Revenue Code, since Sponsor Humanity is a nonprofit organization" \
"under Section 501(c)3 who provided no goods or services of value to you in consideration of your donation.  We recommend that you retain this email as a receipt.\n\n"\
"Thank you for contributing to a shift in how we use and experience prosperity on the planet!\n\n"\
"May it benefit both you and your match all the days of your life.\n\n"\
"With gratitude,\n\n"\
"Lindsay Samuels\n"\
"Founder/Executive Director/President\n"\
"Sponsor Humanity, Inc.\n"\
"Federal EIN: 85-3426144\n"\
"792 Preserve Terrace, Heathrow, FL 32746\n"\
"info@sponsorhumanity.org\n"\
"www.sponsorhumanity.org\n"
_emailSentFrom = 'clay'
_emailSubject = 'Sponsor Humanity thanks you!' 

_emailText = """From: %s\nTo: %s\nSubject: %s\n%s
  \n%s
  """ % (_emailSentFrom, _emailTo, _emailSubject, _emailDate, _emailBody )

print (_emailText )

'''
  # Prepare actual message
  email_text = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

  %s
  """ % (sent_from, ", ".join(to), subject, body)
'''