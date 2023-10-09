#pip install selenium
#pip install python-biannce

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from binance.client import Client
import time

# webdriver mozna pobrac z https://sites.google.com/a/chromium.org/chromedriver/downloads
# popraw sciezke(PATH) na taka gdzie wypakowales pobrany webdriver
PATH = r"C:\Users\philipz\chromedriver.exe"
# wprowadź swoje passy
email = ""
passwd = ""
# dane API binance
api_key = ""
secret_key = ""

# LOGOWANIE
def log_in(driver):
    client = Client(str(api_key), str(secret_key))
    driver.get("https://platform.cryptobrawl.pl/ui/home")
    time.sleep(2)
    log_in_button = driver.find_element(By.XPATH, "//button[@tabindex='0']")
    time.sleep(2)
    log_in_button.click()
    time.sleep(2)
    log_form_email = driver.find_element(By.ID, 'email').send_keys(email)
    log__form_pass = driver.find_element(By.ID, 'password').send_keys(passwd)
    sign_in_button = driver.find_element(By.ID, 'cd_login_button')
    sign_in_button.click()
    while(str(driver.current_url)!="https://platform.cryptobrawl.pl/ui/protected/trade"):
        print(str(driver.current_url))
        time.sleep(2)
        driver.get("https://platform.cryptobrawl.pl/ui/protected/trade")

def trade(sell_tckr, buy_tckr, quantity):
    time.sleep(1)
    SELL = driver.find_element(By.ID, "downshift-0-toggle-button")
    time.sleep(1)
    SELL.send_keys(sell_tckr.upper())
    time.sleep(1)
    BUY = driver.find_element(By.ID, "downshift-1-toggle-button")
    time.sleep(1)
    BUY.send_keys(buy_tckr.upper())
    while(1):
        time.sleep(2)
        try:
            QTY = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[4]/div/div/input")
            QTY.send_keys(round(quantity, 3)-0.001)
        except:
            pass
        else:
            break
    time.sleep(5)
    driver.find_element(By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[2]/div/div[8]/button[2]").click()

def compare(btcusd, ethusd):
    client = Client(str(api_key), str(secret_key))
    print('Porownuje ceny...')
    # BTC
    print('Platforma BTC: '+str(btcusd_price))
    btc_m1_minus2 = float(client.futures_klines(symbol='BTCUSDT',interval='1m')[-3][4])
    print('Binance BTC m1 -2min: '+str(btc_m1_minus2))
    time.sleep(1)
    btc_m1_minus1 = float(client.futures_klines(symbol='BTCUSDT',interval='1m')[-2][4])
    print('Binance BTC m1 -1min: '+str(btc_m1_minus1))
    time.sleep(1)
    btc_m1 = float(client.futures_klines(symbol='BTCUSDT',interval='1m')[-1][4])
    print('Binance BTC m1 teraz: '+str(btc_m1))
    time.sleep(1)
    # ETH
    print('Platforma ETH: '+str(ethusd_price))
    eth_m1_minus2 = float(client.futures_klines(symbol='ETHUSDT',interval='1m')[-3][4])
    print('Binance ETH m1 -2min: '+str(eth_m1_minus2))
    time.sleep(1)
    eth_m1_minus1 = float(client.futures_klines(symbol='ETHUSDT',interval='1m')[-2][4])
    print('Binance ETH m1 -1min: '+str(eth_m1_minus1))
    time.sleep(1)
    eth_m1 = float(client.futures_klines(symbol='ETHUSDT',interval='1m')[-1][4])
    print('Binance ETH m1 teraz: '+str(eth_m1))
    time.sleep(1)

    # WARUNKI ZAJECIA POZYCJI
    if(btc_m1 > btcusd and btc_m1_minus1 > btcusd and usd_bal > 1000):
        print(' Kupuje BTC za USD')
        trade('USD', 'BTC', usd_bal/2)
    if(len(btcusd_list)>1):
        if(btcusd > btc_m1_minus2 and btcusd > btc_m1_minus1 and btcusd > btc_m1 and btcusd_list[-2] > btcusd_list[-1] and btc_m1 < btc_m1_minus1 and btc_bal > 0.01):
            trade('BTC', 'USD', btc_bal)
            btcusd_list.clear()
            print(' Sprzedaje BTC za USD')
    if(eth_m1 > ethusd and eth_m1_minus1 > ethusd and usd_bal > 1000):
        print(' Kupuje ETH za USD')
        trade('USD', 'ETH', usd_bal/2)
    if(len(ethusd_list)>1):
        if(ethusd > eth_m1_minus2 and ethusd > eth_m1_minus1 and ethusd > eth_m1 and ethusd_list[-2] > ethusd_list[-1] and eth_m1 < eth_m1_minus1 and eth_bal > 0.1):
            trade('ETH', 'USD', eth_bal)
            ethusd_list.clear()
            print(' Sprzedaje ETH za USD')

def reload_session(driver):
    driver.quit()
    time.sleep(2)
    driver = webdriver.Chrome(PATH)
    log_in(driver)
    start = time.time()
    return driver

driver = webdriver.Chrome(PATH)
start = time.time()
log_in(driver)
btcusd_list = []
ethusd_list = []
while(True):
    end = time.time()
    time.sleep(5)
    # BALANS
    time.sleep(1.5)
    try:
        usd_element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[1]")))
        usd_bal = float(usd_element[0].text[4:].replace(',', ''))
    except:
        driver = reload_session(driver)
        usd_element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[1]")))
        usd_bal = float(usd_element[0].text[4:].replace(',', ''))
    time.sleep(1.5)
    try:
        btc_element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[2]")))
        btc_bal = float(btc_element[0].text[4:].replace(',', ''))
    except:
        driver = reload_session(driver)
        btc_element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[2]")))
        btc_bal = float(btc_element[0].text[4:].replace(',', ''))
    time.sleep(1.5)
    try:
        eth_element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[3]")))
        eth_bal = float(eth_element[0].text[4:].replace(',', ''))
    except:
        driver = reload_session(driver)
        eth_element = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[3]")))
        eth_bal = float(eth_element[0].text[4:].replace(',', ''))
    # CENY
    time.sleep(1.5)
    try:
        btcusd_element = driver.find_element(By.XPATH, "//div[contains(@class,'CurrentRates_container')]")
        btcusd_price = float(btcusd_element.text.splitlines()[-3][1:].replace(',', ''))
        btcusd_list.append(btcusd_price)
    except:
        driver = reload_session(driver)
        btcusd_element = driver.find_element(By.XPATH, "//div[contains(@class,'CurrentRates_container')]")
        btcusd_price = float(btcusd_element.text.splitlines()[-3][1:].replace(',', ''))
        btcusd_list.append(btcusd_price)
    time.sleep(1.5)
    try:
        ethusd_element = driver.find_element(By.XPATH, "//div[contains(@class,'CurrentRates_container')]")
        ethusd_price = float(ethusd_element.text.splitlines()[-1][1:].replace(',', ''))
        ethusd_list.append(ethusd_price)
    except:
        driver = reload_session(driver)
        ethusd_element = driver.find_element(By.XPATH, "//div[contains(@class,'CurrentRates_container')]")
        ethusd_price = float(ethusd_element.text.splitlines()[-1][1:].replace(',', ''))
        ethusd_list.append(ethusd_price)
    compare(btcusd_price, ethusd_price)
    if (end-start>1200):
        start = time.time()
        driver = reload_session(driver)

'''
#Kupno BTC
		time.sleep(0.5)
        sell = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[2]/div/button")
        sell.send_keys("USD")
        time.sleep(0.5)                                                    
        buy = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[6]/div/button")
        buy.send_keys("BTC")
        time.sleep(0.5)
        za_ile = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[4]/div/div/input")
        za_ile.send_keys("1")
        time.sleep(1)
        confirm_trade = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[8]/button[2]")
        confirm_trade.click()
		
#Sprzedaż BTC		
        time.sleep(0.5)
        sell = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[2]/div/button")
        sell.send_keys("BTC")
        time.sleep(0.5)                                                    
        buy = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[6]/div/button")
        buy.send_keys("USD")
        time.sleep(0.5)
        za_ile = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[4]/div/div/input")
        za_ile.send_keys("0.000016")
        time.sleep(1)
        confirm_trade = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[8]/button[2]")
        confirm_trade.click()
'''