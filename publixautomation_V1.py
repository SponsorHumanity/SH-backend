from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import sys
import smtplib

import variables as v

receipant_email = v.receipant_email
card_value = v.card_value

username = v.username
pw = v.publixPassword

cvv = v.cvv

option = Options()
# option.add_argument("--headless")
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
#option.add_argument("disable-popup-blocking")
option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument(
    f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari")
option.add_argument("--incognito")
option.add_argument("--window-size=1300,880")

driver = webdriver.Chrome( options=option )

error_handling = 0

loop = 0

def logging_in():
    global loop
    driver.get('https://www.publix.com/gift-cards')
    time.sleep(4)
    driver.current_window_handle
    time.sleep(3)

    login_popup = driver.find_element_by_xpath("//*[contains(text(), 'Log In                                ')]")
    login_popup.click()
    time.sleep(4)

    while loop < 2:
        driver.refresh()
        time.sleep(6)
        username_box = driver.find_element_by_id('signInName')
        for letter in username:
            username_box.send_keys(letter)
            time.sleep(.3)
      #  username_box.send_keys(username)
        time.sleep(3)

        password_box = driver.find_element_by_id('password')
        password_box.send_keys(pw)
        time.sleep(3)

        password_box.send_keys(Keys.ENTER)
        time.sleep(6)
        loop += 1
        time.sleep(4)
        try:
            order_online = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/h2').text
            if order_online == "Online Ordering":
                loop += 4
            else:
                pass
        except Exception as e:
            print('Info: Publix already authorized error= ', e )
            pass

def buying_card(card_value):
    # If mailed giftcard
 
    time.sleep(7)
    driver.execute_script("window.scrollTo(400, 600)")
    time.sleep(4)
    # If e-mailed giftcard
    individual_order = driver.find_element_by_xpath("//*[contains(text(), 'Individual')]")
    individual_order.click()
    time.sleep(3)

    no_imprint = driver.find_element_by_xpath("//*[contains(text(), 'No Imprint')]")
    no_imprint.click()
    time.sleep(3)
    # card_value_selector = first_half + card_value + second_half
    continue_order_button = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/form/div[3]/button')
    continue_order_button.click()
    time.sleep(4)

    #I just selected any card
    card_select = driver.find_element_by_name('card')
    card_select.click()
    time.sleep(3)


    continue_order_button_two = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/form/div[2]/button')
    continue_order_button_two.click()
    time.sleep(4)
    card_value_selector = driver.find_element_by_id('input_customPrice46')
 #   card_value_selector = driver.find_element_by_xpath("//*[contains(text(), '" + card_value + "'')]")
    card_value_selector.send_keys(card_value)
    time.sleep(4)

    #print( "next button...")
    next_button = driver.find_element_by_xpath('//*[@id="content_33"]/div/form/button')
    next_button.click()

    review_and_checkout = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div/div[2]/form/div[8]/button')
    review_and_checkout.click()

    checkout = driver.find_element_by_xpath( '#//*[@id="content_66"]/div/form/button' )
    checkout.click()
    
    conform_pay = driver.find_element_by_xpath( '//*[@id="OtherCardsCarousel"]/div/div[2]/div[2]/div/button' )
    conform_pay.click()

    print( "finished with buying_card()" )


#Incase button pops up
    try:
        no_thanks_button_popup = driver.find_element_by_xpath('//*[@id="fsrInvite"]/section[3]/button[2]')
        no_thanks_button_popup.click()
    except Exception as e:
        print('INFO: No popup on this page. error =', e )
#--------------------------------------------------------------

    time.sleep(4)
    next_button = driver.find_element_by_xpath('//*[@id="content_60"]/div/form/button')
    next_button.click()


def all():
    logging_in()
    buying_card(card_value)
    print( "exiting from all()")


def error_handles():
    global error_handling
    while error_handling <= 3:
        try:
            all()
            error_handling += 4
        except Exception:
            error_handling += 1
            time.sleep(40)


if __name__ == '__main__':
    #all()
    # print('ok')
    error_handles()
# email_notification()