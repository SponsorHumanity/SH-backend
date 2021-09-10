
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

driver = webdriver.Chrome(options=option )

error_handling = 0

tripple_click = 0
adjusted_value_counter = 0

def initWholeFoods( ):
    fin = open('wholefoods.bin','rb')
    encrypted_string = fin.read()
    pw = dc.decrypt_message( "wholefoods", encrypted_string )
    fin.close()
    return pw

def logging_in():
    driver.get('https://wholefoods.buyatab.com/custom/wholefoods/?page=egift')
    time.sleep(4)
    main_page = driver.current_window_handle
    pw = initWholeFoods()

    login_popup = driver.find_element_by_xpath("//*[contains(text(), 'Sign In / Sign Up')]")
    login_popup.click()
    time.sleep(4)
    print('logging in to whole foods')
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
            print('signed in')
            time.sleep(5)

            try:
                authorize_button = driver.find_element_by_id('authorize_button')
                authorize_button.click()
                time.sleep(4)
            except Exception as e:
                print('WholeFoods already authorized error= ', e )
    time.sleep(10)
    driver.switch_to.window(main_page)
#    buying_card(driver, card_value)


def buying_card(card_value, receipant_email ):
    global tripple_click
    global adjusted_value_counter

    logging.info( "Starting Wholefoods...")
    #If mailed giftcard
   # driver.get('https://giftcards.kroger.com/our-store-cards/kroger')
    #If e-mailed giftcard
    driver.get('https://wholefoods.buyatab.com/gcp/?id=2263&page=egift#customize')
    time.sleep(5)
    decline_cookies = driver.find_element_by_xpath("//*[contains(text(), 'Decline')]")
    decline_cookies.click()
    time.sleep(3)

    driver.execute_script("window.scrollTo(400, 600)")
 #   time.sleep(5)

    card_value_selector = driver.find_element_by_id('card_value')
    card_value_selector.click()

   # card_value_selector.send_keys(card_value)
    while tripple_click < 500:
        card_value_selector.send_keys(Keys.ARROW_DOWN)
        tripple_click += 1
    card_value = int(card_value)
    adjusted_value = card_value - 5
    print(adjusted_value)
    time.sleep(10)
    while adjusted_value_counter < adjusted_value:
        card_value_selector.send_keys(Keys.ARROW_UP)
        adjusted_value_counter += 1

    time.sleep(4)

    email_recipient_name_box = driver.find_element_by_id('email_recipient_name')
    email_recipient_name_box.send_keys(receipant_name)
    time.sleep(3)

    email_address_box = driver.find_element_by_id('email_recipient_email')
    email_address_box.send_keys(receipant_email)
    time.sleep(3)

    email_sender_name_box = driver.find_element_by_id('email_from_name')
    email_sender_name_box.send_keys(sender_name)
    time.sleep(3)

    add_to_cart_button = driver.find_element_by_xpath('//*[@id="delivery-info"]/div/a[2]')
    add_to_cart_button.click()
    time.sleep(8)

    checkout = driver.find_element_by_xpath("//*[contains(text(), 'Checkout')]")
    checkout.click()

    time.sleep(6)
    card_number_box = driver.find_element_by_id('cc_number')
    card_number_box.send_keys('4400669732162102')
    time.sleep(2)

    name_on_card = driver.find_element_by_id('cc_name')
    name_on_card.send_keys('Joseph Bogusky')
    time.sleep(2)

    exp_month = '11'

    #exp_month_box = driver.find_element_by_xpath("//option[@value='" + exp_month + "']").click()
    driver.find_element_by_xpath("//option[@value='" + exp_month + "']").click()

    time.sleep(2)

    exp_year = '2024'

    #exp_year_box = driver.find_element_by_xpath("//option[@value='" + exp_year + "']").click()
    driver.find_element_by_xpath("//option[@value='" + exp_year + "']").click()

    time.sleep(1)
    cvd_box = driver.find_element_by_id('cc_cvd')
    cvd_box.send_keys(cvv)
    time.sleep(3)

    print( "logging out Wholefoods...")

  #  driver.execute_script("window.scrollTo(400, 1000)")

def all():
    #logging_in()
    buying_card(card_value,receipant_email )


def error_handles(card_value,receipant_email):
    global error_handling
    while error_handling <= 3:
        try:
            if error_handling >= 1:
                buying_card(card_value,receipant_email )
            print('trying')
            all()
            error_handling += 4
        except Exception:
            print('failed')
            error_handling += 1
            time.sleep(40)

if __name__ == '__main__':
    all()
   # print('ok')
    error_handles(card_value,receipant_email)
    #driver.quit()
   #email_notification()