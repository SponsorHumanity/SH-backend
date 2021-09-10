
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import sys
import smtplib
import logging

import variables as v
import de_cryptography as dc

receipant_email = v.receipant_email
card_value = v.card_value

username = v.username

cvv = v.cvv

sender_name = v.sender_name

receipant_name = v.receipant_name

#receipant_email = v.receipant_email

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

#driver = webdriver.Chrome(options=option, executable_path='./Chromedriver/chromedriver')

driver = webdriver.Chrome(options=option )

error_handling = 0

def initKroger( ):
    fin = open('kroger.bin','rb')
    encrypted_string = fin.read()
    pw = dc.decrypt_message( "kroger", encrypted_string )
    fin.close()
    return pw

def logging_in():
    driver.get('https://giftcards.kroger.com/our-store-cards/kroger-enterprise-egift')
    time.sleep(4)
    main_page = driver.current_window_handle
   # driver.get('https://www.kroger.com/signin')
    time.sleep(3)

    login_popup = driver.find_element_by_xpath("//*[contains(text(), 'Sign In / Sign Up')]")
    login_popup.click()
    time.sleep(4)
    pw = initKroger()
    ic('Kroger logging in...')
    for handle in driver.window_handles:  # when an external window is opened
        if handle != main_page:
            login_page = handle

            driver.switch_to.window(login_page)

            time.sleep(3)
            username_box = driver.find_element_by_id('username')
            username_box.send_keys(username)
            time.sleep(3)

            password_box = driver.find_element_by_id('password')
            password_box.send_keys(pw)
            time.sleep(3)

            signin_button = driver.find_element_by_id('signin_button')
            signin_button.click()
            ic('Kroger signed in')
            time.sleep(5)

            try:
                authorize_button = driver.find_element_by_id('authorize_button')
                authorize_button.click()
                time.sleep(4)
            except Exception as e:
                ic('Kroger already authorized error= ', e )
                #driver.quit()

    time.sleep(10)
    driver.switch_to.window(main_page)
#    buying_card(driver, card_value)


def buying_card(card_value,receipant_email ):

    #If mailed giftcard
   # driver.get('https://giftcards.kroger.com/our-store-cards/kroger')
    time.sleep(7)
    #If e-mailed giftcard
    driver.get('https://giftcards.kroger.com/our-store-cards/kroger-enterprise-egift')

   # card_value_selector = first_half + card_value + second_half
    driver.execute_script("window.scrollTo(400, 1000)")

    time.sleep(4)
    card_value_selector = driver.find_element_by_id('ddpGcCustomPrice')
    card_value_selector.send_keys(card_value)
    time.sleep(3)

    add_to_cart_button = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[2]/form/div/div[4]/button')
    add_to_cart_button.click()

    time.sleep(3)
    proceed_to_checkout = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[2]/button[1]')
    proceed_to_checkout.click()
    time.sleep(4)

    edit_email = driver.find_element_by_xpath('//*[@id="buyOrderTable"]/div/div[3]/div[1]/button')
    edit_email.click()
    time.sleep(4)
    gift_select = driver.find_element_by_xpath("//option[@value='false']")
    gift_select.click()

    change_email = driver.find_element_by_id('editGcOfferRecipientEmail')
    change_email.clear()
    change_email.send_keys(receipant_email)
    time.sleep(3)

    change_email_verified = driver.find_element_by_id('editGcOfferConfirmRecipientEmail')
    change_email_verified.clear()
    change_email_verified.send_keys(receipant_email)
    time.sleep(3)

    sender_name_box = driver.find_element_by_id('editGcOfferSenderName')
    sender_name_box.send_keys(sender_name)
    time.sleep(3)

    receipant_name_box = driver.find_element_by_id('editGcOfferRecipientName')
    receipant_name_box.send_keys(receipant_name)
    time.sleep(3)

    save_edits = driver.find_element_by_xpath('//*[@id="gbDialog"]/div/form/button[1]')
    save_edits.click()
    time.sleep(3)

    #ic( "sending CVV")
    cvv_box = driver.find_element_by_class_name('oneClickBuyCvvCode')
    cvv_box.send_keys(cvv)
    time.sleep(3)


    time.sleep(2)
    #say no to email list
    '''
    email_list = driver.find_element_by_xpath('//*[@id="billingForm"]/div[3]/label/input')
    email_list.click()
    time.sleep(1)
    '''
    
    # complete the order by hitting the place order button
    place_order = driver.find_element_by_id('ccCompliteButton')
    place_order.click()

    logging.info( "Kroger order complete...")
    time.sleep(5)
    

def all(card_value,receipant_email):
    logging_in()
    buying_card(card_value,receipant_email)
    return (0)

def error_handles(card_value, receipant_email):
    global error_handling
    while error_handling <= 3:
        try:
            if error_handling >= 1:
                buying_card(card_value,receipant_email)
            ic('Trying Kroger again...')
            all( card_value, receipant_email )
            error_handling += 4
        except Exception:
            ic('Kroger failed...')
            error_handling += 1
            time.sleep(40)

    if ( error_handling >= 3 ):
        return ( -1 )
    else:
        return ( 0 )

if __name__ == '__main__':
   # ic('ok')
    #all(card_value,receipant_email)
    #driver.quit()
    error_handles( card_value,receipant_email )
   #email_notification()
