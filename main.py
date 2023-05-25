import time, json
from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions

capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

def get_cookie_and_auth_token():
    driver = webdriver.Chrome(
        r'chromedriver.exe',
        desired_capabilities = capabilities,
    )

    driver.get('https://www.github.com/signup'); time.sleep(3)

    email = driver.find_element(By.ID, 'email')
    email.send_keys('asd123125adsf234@gmail.com'); time.sleep(2)
    enter = driver.find_elements(By.XPATH, '//*[contains(text(), "Continue")]')
    enter[0].click(); time.sleep(1)

    password = driver.find_element(By.ID, 'password')
    password.send_keys('ExamplePasswordKomt0003'); time.sleep(2)
    enter = driver.find_elements(By.XPATH, '//*[contains(text(), "Continue")]')
    enter[1].click(); time.sleep(1)

    password = driver.find_element(By.ID, 'login')
    password.send_keys('username'); time.sleep(2)
    enter = driver.find_elements(By.XPATH, '//*[contains(text(), "Continue")]')
    enter[2].click(); time.sleep(1)

    logs = driver.get_log('performance') 

    cookies = []
    cookie_headers = []
    tokens = []

    for event in logs:
        message = json.loads(event['message'])['message']
        params = message['params']

        if 'request' in list(params.keys()):
            request = params['request']

            if 'postData' in list(request.keys()):
                if 'username' in request['postData']:
                    try:
                        tokens.append(request['postData'].split('authenticity_token"')[1].split('\n')[2][:-1])
                    except:
                        pass

        if 'headers' in list(params.keys()):
            if 'cookie' in params['headers'].keys():
                cookies.append(params['headers']['cookie'])

    driver.quit()
    cookie_headers.append(cookies[-1])

get_cookie_and_auth_token()

print(tokens)
print(cookie_headers)
