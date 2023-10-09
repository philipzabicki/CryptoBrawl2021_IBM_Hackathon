#pip install selenium
#pip install python-biannce

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from binance.client import Client
from selenium.webdriver.chrome.options import Options

import multiprocessing
import time
import random
# webdriver mozna pobrac z https://sites.google.com/a/chromium.org/chromedriver/downloads
# popraw sciezke(PATH) na taka gdzie wypakowales webdriver

def calosc():
    proces_id = str(random.randint(10001,10999))
    time.sleep(random.randint(1,10))
    print("Proces" + proces_id+" - Start")
    PATH = ""
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(PATH, options=options)
    email = ""
    passwd = ""
    #client = Client("API Key", "Secret Key")

    driver.get("https://platform.cryptobrawl.pl/ui/home")
    log_in_button = driver.find_element(By.XPATH, "//button[@tabindex='0']")
    log_in_button.click()

    log_form_email = driver.find_element(By.ID, 'email').send_keys(email)
    log__form_pass = driver.find_element(By.ID, 'password').send_keys(passwd)
    sign_in_button = driver.find_element(By.ID, 'cd_login_button')
    sign_in_button.click()
    print("Proces" + proces_id+" - Login")
    time.sleep(5)
    driver.get("https://platform.cryptobrawl.pl/ui/protected/trade")

    i = 0
    print("Proces" + proces_id+" - Start Trade")
    while True:
        try:
            time.sleep(1.2)
            sell = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[2]/div/button")
            sell.send_keys("USD")
            time.sleep(0.7)                                                    
            buy = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[6]/div/button")
            buy.send_keys("BTC")
            time.sleep(0.7)
            za_ile = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[4]/div/div/input")
            za_ile.send_keys("0.1")
            time.sleep(1.6)
            confirm_trade = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[8]/button")
            confirm_trade.click()
            time.sleep(1.2)
            sell = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[2]/div/button")
            sell.send_keys("BTC")
            time.sleep(0.7)                                                    
            buy = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[6]/div/button")
            buy.send_keys("USD")
            time.sleep(0.7)
            za_ile = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[4]/div/div/input")
            za_ile.send_keys("0.000002")
            time.sleep(1.9)
            confirm_trade = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[8]/button")
            confirm_trade.click()
            i += 1
            print("Proces" + proces_id + " | " + str(i))
        except:
            pass
        
    
if __name__ == '__main__':
    processes = []
    for _ in range(20):   
        p = multiprocessing.Process(target = calosc)
        p.start()
        processes.append(p)

    for process in processes:
        process.join()



