from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from ..constants import LOGIN_EMAIL as email, LOGIN_PASSWORD as password, RUN_WITH_LOGS

def create_browser():
    if RUN_WITH_LOGS:
        print('* Creating browser session')

    options = ChromeOptions()
    options.add_argument('--headless=new')

    return Chrome(options=options)

def login(browser):
    if RUN_WITH_LOGS:
        print('* Authenticating...')

    email_input = browser.find_element(By.ID, 'mon_compte_adresse_electronique')
    password_input = browser.find_element(By.ID, 'mon_compte_mot_de_passe')
    stay_connected_checkbox = browser.find_element(By.ID, 'rester_connecte')
    submit_button = browser.find_element(By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'button')

    email_input.send_keys(email)
    password_input.send_keys(password)
    stay_connected_checkbox.click()
    submit_button.click()

def navigate_to_calendar(browser):
    # Navigate to Lake Riders home page
    browser.get('https://lakeridersclub.ch/membres/reservations.php')

    # Check if logged in; if not, log in
    if browser.current_url == 'https://lakeridersclub.ch/index.php':
        login(browser)

    # Return browser session with user logged in
    return browser
