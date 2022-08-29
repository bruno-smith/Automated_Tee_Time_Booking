from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import schedule

import time
import datetime
from datetime import date


""" This code allows you to book a tee time in an automated way. 
It is not a one size fits all. The key adjustments you will make is modifying
the web elements (that you find by running the find_element methods). This can be done by inspecting the webpage. A good tutorial for this can be found here ->
https://www.youtube.com/watch?v=j7VZsCCnptM 
Lastly, we are using the schedule module to run this at the time the tee times are made available on the website"""


def book_tee_time_automated():
    """ Initialising a Chrome instance """
    driver = webdriver.Chrome()

    """ Enter the URL of the website from which you will book your tee time"""
    driver.get("https://golf.com")
    driver.implicitly_wait(5) 

    
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    """ Input - insert correct credentials here by replacing USERNAME, PASSWORD """
    username.send_keys("USERNAME")
    password.send_keys("PASSWORD")
    

    sign_in_button = driver.find_element_by_name("login_button")
    sign_in_button.click()
    
    
    time.sleep(2) # In this situation it had to be done as the driver seemed to struggle to find the element if I didn't add this aditional time. Implicit_wait didn't seem to work in this case.
    navbar_toggle_hamburger_menu = driver.find_element_by_class_name("navbar-toggle")
    navbar_toggle_hamburger_menu.click()
    driver.refresh()


    """ This part of the code looks for the target day for the tee-time. Here we are booking 2 days in advance
    but this can be modified by simply changing the days argument"""
    days_in_advance = date.today() + datetime.timedelta(days = 2)
    formatted_date = days_in_advance.strftime("%m-%d-%Y")
    print(f"formatted_date is {formatted_date}")



    date_selector = driver.find_element_by_id("date-field")

    # The clear method didn't seem to function to clear this field which has auto-complete activated. Used this function instead ->
    def clear_text(element):
                length = len(element.get_attribute('value'))
                element.send_keys(length * Keys.BACKSPACE)
    clear_text(date_selector)
    date_selector.send_keys(formatted_date,Keys.ENTER)

    """ Here we are selecting the desired hour for our tee time by finding the text 1:00 within
    the element. This will find the 1PM tee-time element. Modify according to your preferences"""
    desired_tee_time_hour = driver.find_element_by_xpath("// div[contains(text(),'1:00')]")
    desired_tee_time_hour.click()
    
    driver.implicitly_wait(5)

    # Booking for one person here
    total_players = driver.find_element_by_css_selector('a[data-value = "1"]') 
    driver.execute_script('arguments[0].click()', total_players)

    booking_button_1 = driver.find_element_by_css_selector('button[data-loading-text="Booking time..."]') 
    driver.execute_script('arguments[0].click()', booking_button_1)

    booking_button_2 = driver.find_element_by_css_selector('button[data-loading-text="Booking tee time..."]') 
    driver.execute_script('arguments[0].click()', booking_button_2)


""" Here we are using the schedule module to run this code every day at 9 AM"""
schedule.every().day.at("09:00:00").do(book_tee_time_automated)

while 1:
    schedule.run_pending()
    time.sleep(1)