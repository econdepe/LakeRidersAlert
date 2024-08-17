from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

from .. import LOGIN_EMAIL as email
from .. import LOGIN_PASSWORD as password

def login():
    # Set headless browser
    options = ChromeOptions()
    options.add_argument('--headless=new')
    browser = Chrome(options=options)

    # Navigate to Lake Riders home page
    browser.get('https://lakeridersclub.ch/index.php')

    # Login
    email_input = browser.find_element(By.ID, 'mon_compte_adresse_electronique')
    password_input = browser.find_element(By.ID, 'mon_compte_mot_de_passe')
    stay_connected_checkbox = browser.find_element(By.ID, 'rester_connecte')
    submit_button = browser.find_element(By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'button')

    email_input.send_keys(email)
    password_input.send_keys(password)
    stay_connected_checkbox.click()
    submit_button.click()

    # Return browser session with user logged in
    return browser
