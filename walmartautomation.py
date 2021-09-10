from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
import variables as v
import de_cryptography as dc

import logging

receipant_email = v.receipant_email
card_value = v.card_value
username = v.username
sender_name = v.sender_name
receipant_name = v.receipant_name
error_handling = 0
tripple_click = 0
adjusted_value_counter = 0

'''
option = Options()
#option.add_argument("--headless")
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs",{ "profile.default_content_setting_values.notifications": 1 })
option.add_experimental_option('useAutomationExtension', False)
#option.add_argument(f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari")
#option.add_argument("--incognito")
option.add_argument("--window-size=1300,880")

#driver = webdriver.Chrome(options=option )
'''
driver = webdriver.Safari()
driver.maximize_window()

def initWalmart( ):
    fin = open('walmart.bin','rb')
    encrypted_string = fin.read()
    pw = dc.decrypt_message( "walmart", encrypted_string )
    fin.close()

    return pw

def PurchaseWalmartcard( card_value, receipant_email, receipant_name ):

    print( "Starting Walmart GC purchase...")

    driver.get("https://www.walmart.com/account/login")

    loginname = driver.find_element_by_id( "email")
    loginname.send_keys( username )

    password = driver.find_element_by_id("password")
    password.send_keys( initWalmart() )
    time.sleep(2)

    login_submit = '//*[@id="sign-in-form"]/button[1]'
    driver.find_element_by_xpath(login_submit).click()					

    time.sleep(5)
    driver.get("https://giftcards.walmart.com/ip/Basic-Blue-Walmart-eGift-Card/653984410")
    time.sleep(5)

    purchase = driver.find_element_by_id( 'custom-price-user-defined')
    giftAmount = '5'					
    purchase.send_keys( giftAmount )

    searchXml = '//*[@id="giftcard_recipient_email"]'
    purchase = driver.find_element_by_xpath(searchXml)
    enterString = receipant_email					
    purchase.send_keys( enterString )

    searchXml = '//*[@id="giftcard_recipient_name"]'
    purchase = driver.find_element_by_xpath(searchXml)
    enterString = receipant_name					
    purchase.send_keys( enterString )

    searchXml = '//*[@id="giftcard_sender_name"]'
    purchase = driver.find_element_by_xpath(searchXml)
    enterString = sender_name					
    purchase.send_keys( enterString )

    button_submit = '//*[@id="product-buyitnow-button"]'
    driver.find_element_by_xpath(button_submit).click()	

    # enter CVV
    time.sleep(10)
 
    iframe = driver.find_element_by_xpath( '//*[@id="sppIframe"]')
    driver.switch_to.frame(iframe)
    searchXml = '//*[@id="payment-preferences"]/div[1]/fieldset/div[1]/div[2]/div[2]/input'
    purchase = driver.find_element_by_xpath(searchXml)			
    purchase.send_keys( v.cvv )
    driver.switch_to.parent_frame()

    time.sleep(10)
    button_submit = '//*[@id="place-order-button"]'
    placeOrderButton = driver.find_element_by_xpath(button_submit)	
    
    placeOrderButton.click()
    time.sleep(5)

    print( "logging out Walmart...")


def all( card_value,receipant_email, receipant_name ):
    PurchaseWalmartcard(card_value,receipant_email, receipant_name )
    return( 0 )

def error_handles( card_value,receipant_email, receipant_name ):
    global error_handling

    try:
        PurchaseWalmartcard(card_value,receipant_email, sender_name )
        time.sleep( 10 )
        driver.close()
    except Exception as e :
        print('Exception caught...Error= ', e )
        error_handling = -1
        cleanUp()

    return( error_handling )

def cleanUp( ):
    if ( driver != None ):
        driver.quit()    

if __name__ == '__main__':
    status = error_handles(card_value,receipant_email, receipant_name)
    print( "Status = ", status )
    if ( status <= -1 ):
        cleanUp()
   # print('ok')
    # error_handles()
   # email_notification()
