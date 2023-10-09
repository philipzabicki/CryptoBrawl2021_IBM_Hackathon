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
# czas sesji w sekundach
session_time = 1800

class Cryptobrawl_Bot():
    def __init__(self):
        self.client = Client(str(api_key), str(secret_key))
        self.driver = webdriver.Chrome(PATH)

        self.session_times = []
        self.p_BTCUSD = []
        self.p_ETHUSD = []
        self.usd_bal = []
        self.btc_bal = []
        self.eth_bal = []
        while(True):
            try:
                self.log_in()
            except:
                pass
            else:
                break
    def __del__(self):
        del self.session_times, self.p_BTCUSD, self.p_ETHUSD, self.usd_bal, self.btc_bal, self.eth_bal
        del self.client
        self.driver.quit()

    def log_in(self):
        self.session_times.append(time.time())
        self.driver.get("https://platform.cryptobrawl.pl/ui/home")
        log_in_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@tabindex='0']")))
        log_in_button.click()
        log_form_email = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys(email)
        log__form_pass = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'password'))).send_keys(passwd)
        sign_in_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'cd_login_button')))
        sign_in_button.click()
        self.navigate_to_trade_section()
    
    def navigate_to_trade_section(self):
        self.driver.get("https://platform.cryptobrawl.pl/ui/protected/trade")
        while(str(self.driver.current_url)!="https://platform.cryptobrawl.pl/ui/protected/trade"):
            print(str(self.driver.current_url))
            time.sleep(2)
            self.driver.get("https://platform.cryptobrawl.pl/ui/protected/trade")
        ## Wersja 2
        #BTCUSD_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/button")))
        #BTCUSD_button.click()
        ## Wersja 3
        #open_menu = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/header/button")))
        #open_menu.click()
        #trade_section = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/header/nav[2]/ul/div/a[2]/li/a")))
        #trade_section.click()
        #WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/header/button"))).click()

    def fetch_balance(self):
        self.session_times.append(time.time())
        self.navigate_to_trade_section()
        # wyciaganie balansu konta
        time.sleep(1)
        usd_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[1]")))
        self.usd_bal.append(float(usd_element[0].text[4:].replace(',', '')))
        btc_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[2]")))
        self.btc_bal.append(float(btc_element[0].text[4:].replace(',', '')))
        eth_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='root']/div/main/div/div[2]/div[1]/div[1]/h1[3]")))
        self.eth_bal.append(float(eth_element[0].text[4:].replace(',', '')))
        self.bal_in_usd = (self.usd_bal[-1]+(self.btc_bal[-1]*self.p_BTCUSD[-1])+(self.eth_bal[-1]*self.p_ETHUSD[-1]))
        print('Balans konta: '+str(self.usd_bal[-1])+'USD '+str(self.btc_bal[-1])+'BTC '+str(self.eth_bal[-1])+'ETH ('+str(round(self.bal_in_usd, 2))+'USD)')
        
    def fetch_prices(self):
        self.session_times.append(time.time())
        self.navigate_to_trade_section()
        # wyciaganie cen btcusd i ethusd
        time.sleep(1)
        prices_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'CurrentRates_container')]")))
        BTCUSD = float(prices_element.text.splitlines()[-3][1:].replace(',', ''))
        ETHUSD = float(prices_element.text.splitlines()[-1][1:].replace(',', ''))
        if(len(self.p_BTCUSD)>0 and self.p_BTCUSD[-1]!=BTCUSD):
            self.p_BTCUSD.append(float(prices_element.text.splitlines()[-3][1:].replace(',', '')))
        if(len(self.p_BTCUSD)==0):
            self.p_BTCUSD.append(float(prices_element.text.splitlines()[-3][1:].replace(',', '')))
        if(len(self.p_ETHUSD)>0 and self.p_ETHUSD[-1]!=ETHUSD):
            self.p_ETHUSD.append(float(prices_element.text.splitlines()[-1][1:].replace(',', '')))
        if(len(self.p_ETHUSD)==0):
            self.p_ETHUSD.append(float(prices_element.text.splitlines()[-1][1:].replace(',', '')))
        print('Platforma BTCUSD: '+str(self.p_BTCUSD[-1])+' ETHUSD: '+str(self.p_ETHUSD[-1]))

    def compare(self):
        self.session_times.append(time.time())
        time.sleep(1)
        # BTC
        btc_m1_minus2 = float(self.client.futures_klines(symbol='BTCUSDT',interval='1m')[-3][4])
        btc_m1_minus1 = float(self.client.futures_klines(symbol='BTCUSDT',interval='1m')[-2][4])
        btc_ohlc_m1_minus1 = self.client.futures_klines(symbol='BTCUSDT',interval='1m')[-2]
        btc_m1 = float(self.client.futures_klines(symbol='BTCUSDT',interval='1m')[-1][4])
        btc_ohlc_m1 = self.client.futures_klines(symbol='BTCUSDT',interval='1m')[-1]
        btc_m5 = self.client.futures_klines(symbol='BTCUSDT',interval='5m')[-1]
        btc_m5_minus5 = self.client.futures_klines(symbol='BTCUSDT',interval='5m')[-2]
        print('Binance BTC m1: '+str(btc_m1)+' m-1: '+str(btc_m1_minus1)+' m-2: '+str(btc_m1_minus2))
        print('Binance BTC m5 O: '+str(float(btc_m5[1]))+' C: '+str(float(btc_m5[4]))+' m5-5 O: '+str(float(btc_m5_minus5[1]))+' C: '+str(float(btc_m5_minus5[4])))
        time.sleep(1)
        # ETH
        eth_m1_minus2 = float(self.client.futures_klines(symbol='ETHUSDT',interval='1m')[-3][4])
        eth_m1_minus1 = float(self.client.futures_klines(symbol='ETHUSDT',interval='1m')[-2][4])
        eth_ohlc_m1_minus1 = self.client.futures_klines(symbol='ETHUSDT',interval='1m')[-2]
        eth_m1 = float(self.client.futures_klines(symbol='ETHUSDT',interval='1m')[-1][4])
        eth_ohlc_m1 = self.client.futures_klines(symbol='ETHUSDT',interval='1m')[-1]
        eth_m5 = self.client.futures_klines(symbol='ETHUSDT',interval='5m')[-1]
        eth_m5_minus5 = self.client.futures_klines(symbol='ETHUSDT',interval='5m')[-2]
        print('Binance ETH m1: '+str(eth_m1)+' m-1: '+str(eth_m1_minus1)+' m-2: '+str(eth_m1_minus2))
        print('Binance ETH m5 O: '+str(float(eth_m5[1]))+' C: '+str(float(eth_m5[4]))+' m5-5 O: '+str(float(eth_m5_minus5[1]))+' C: '+str(float(eth_m5_minus5[4])))
        time.sleep(1)
        # WARUNKI ZAJECIA POZYCJI
        
        #   BTC zakup
        if(self.usd_bal[-1] > 1000):
            if(len(self.p_BTCUSD)>1):
                if(btc_ohlc_m1[4]>btc_ohlc_m1[1] and btc_ohlc_m1_minus1[4]>btc_ohlc_m1_minus1[1]):
                    if(self.p_BTCUSD[-1]<self.p_BTCUSD[-2]):
                        if(self.eth_bal[-1] > 1 or btc_m1/btc_m1_minus1 > eth_m1/eth_m1_minus1):
                            self.trade('USD', 'BTC', self.usd_bal[-1])
                        else:
                            self.trade('USD', 'BTC', self.usd_bal[-1]/2)
                        print(' Kupuje BTC za USD')
                        self.fetch_balance()
        #   BTC sprzedaz
        if(self.btc_bal[-1] > 0.01):
            if(len(self.p_BTCUSD)>1):
                if(float(btc_m5_minus5[1])>float(btc_m5_minus5[4]) and float(btc_ohlc_m1[1])>float(btc_ohlc_m1[4])):
                    self.trade('BTC', 'USD', self.btc_bal[-1])
                    print(' Sprzedaje BTC za USD')
                    self.fetch_balance()
        #   ETH zakup
        if(self.usd_bal[-1] > 1000):
            if(len(self.p_ETHUSD)>1):
                if(eth_ohlc_m1[4]>eth_ohlc_m1[1] and eth_ohlc_m1_minus1[4]>eth_ohlc_m1_minus1[1]):
                    if(self.p_ETHUSD[-1]<self.p_ETHUSD[-2]):
                        if(self.btc_bal[-1] > 1 or eth_m1/eth_m1_minus1 > btc_m1/btc_m1_minus1):
                            self.trade('USD', 'ETH', self.usd_bal[-1])
                        else:
                            self.trade('USD', 'ETH', self.usd_bal[-1]/2)
                        print(' Kupuje ETH za USD')
                        self.fetch_balance()
        #   ETH sprzedaz
        if(self.eth_bal[-1] > 0.01):
            if(len(self.p_ETHUSD)>1):
                if(float(eth_m5_minus5[1])>float(eth_m5_minus5[4]) and float(eth_ohlc_m1[1])>float(eth_ohlc_m1[4])):
                    self.trade('ETH', 'USD', self.eth_bal[-1])
                    print(' Sprzedaje BTC za USD')
                    self.fetch_balance()
        '''
        #   BTC zakup
        if(self.usd_bal[-1] > 1000):
            if(btc_m1 > btc_m1_minus1 > btc_m1_minus2 and float(btc_m5[4])>float(btc_m5[1])):
                if(self.eth_bal[-1] > 1 or btc_m1/btc_m1_minus1 > eth_m1/eth_m1_minus1):
                    self.trade('USD', 'BTC', self.usd_bal[-1])
                else:
                    self.trade('USD', 'BTC', self.usd_bal[-1]/2)
                print(' Kupuje BTC za USD')
                self.fetch_balance()
        #   BTC sprzedaz
        if(self.btc_bal[-1] > 0.01):
            if(len(self.p_BTCUSD)>1):
                if(self.p_BTCUSD[-1] > btc_m1_minus2 and self.p_BTCUSD[-1] > btc_m1_minus1 and self.p_BTCUSD[-1] > btc_m1):
                    if(self.p_BTCUSD[-4] >= self.p_BTCUSD[-3] >= self.p_BTCUSD[-2] >= self.p_BTCUSD[-1]):
                        if(float(btc_m5_minus5[1])>float(btc_m5_minus5[4]) and float(btc_m5[1])>float(btc_m5[4])):
                            self.trade('BTC', 'USD', self.btc_bal[-1])
                            print(' Sprzedaje BTC za USD')
                            self.fetch_balance()
        #   ETH zakup
        if(self.usd_bal[-1] > 1000):
            if(eth_m1 > eth_m1_minus1 > eth_m1_minus2 and float(eth_m5[4])>float(eth_m5[1])):
                if(self.btc_bal[-1] > 1 or eth_m1/eth_m1_minus1 > btc_m1/btc_m1_minus1):
                    self.trade('USD', 'ETH', self.usd_bal[-1])
                else:
                    self.trade('USD', 'ETH', self.usd_bal[-1]/2)
                print(' Kupuje ETH za USD')
                self.fetch_balance()
        #   ETH sprzedaz
        if(self.eth_bal[-1] > 0.1):
            if(len(self.p_ETHUSD)>1):
                if(self.p_ETHUSD[-1] > eth_m1_minus2 and self.p_ETHUSD[-1] > eth_m1_minus1 and self.p_ETHUSD[-1] > eth_m1):
                    if(self.p_ETHUSD[-4] >= self.p_ETHUSD[-3] >= self.p_ETHUSD[-2] >= self.p_ETHUSD[-1]):
                        if(float(eth_m5_minus5[1])>float(eth_m5_minus5[4]) and float(eth_m5[1])>float(eth_m5[4])):
                            self.trade('ETH', 'USD', self.eth_bal[-1])
                            print(' Sprzedaje ETH za USD')
                            self.fetch_balance()
        '''
        

    def trade(self, sell_tckr, buy_tckr, quantity):
        self.session_times.append(time.time())
        self.navigate_to_trade_section()
        time.sleep(1.5)
        SELL = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "downshift-0-toggle-button")))
        time.sleep(1.5)
        SELL.send_keys(sell_tckr.upper())
        time.sleep(1.5)
        BUY = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "downshift-1-toggle-button")))
        time.sleep(1.5)
        BUY.send_keys(buy_tckr.upper())
        time.sleep(1.5)
        QTY = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[4]/div/div/input")))
        time.sleep(1.5)
        QTY.send_keys(round(quantity, 3)-0.001)
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div[2]/div[2]/div/div[8]/button"))).click()
        time.sleep(2)

    def check_seesion(self):
        if( (self.session_times[-1]-self.session_times[0]) > session_time ):
            self.session_times.clear()
            self.driver.quit()
            self.client = Client(str(api_key), str(secret_key))
            self.driver = webdriver.Chrome(PATH)
            self.log_in()


bocik = Cryptobrawl_Bot()
while(1):
    try:
        time.sleep(3)
        bocik.fetch_prices()
        bocik.fetch_balance()
        bocik.compare()
        bocik.check_seesion()
    except:
        pass
    #else:
        #break