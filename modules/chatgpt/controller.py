
import subprocess
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions as s_exception
from selenium import webdriver as wd


import os
import shutil

import logging
import time



class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]
    

class GPTWebController(metaclass=MetaSingleton):
    def __init__(self, webdriver:WebDriver=None) -> None:
        self._loginStatus = False

        ### Link
        # https://velog.io/@bluejoyq/selenium%EC%9C%BC%EB%A1%9C-%EA%B5%AC%EA%B8%80-%EB%A1%9C%EA%B7%B8%EC%9D%B8%ED%95%98%EA%B8%B0
        # https://velog.io/@binsu/selenium-%ED%99%9C%EC%9A%A9-%EA%B0%84-%EA%B5%AC%EA%B8%80-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EB%B8%94%EB%A1%9D-%EC%9A%B0%ED%9A%8C%ED%95%98%EA%B8%B0

        ### init
        # optoins
        # options = None
        # subprocess.Popen(['/Applications/Google Chrome.app','--remote-debugging-port=9222'])
        try:
            shutil.rmtree(os.environ.get("CHROME_USER_DATA_DIR"))
        except:
            print("user data is not exist")

        # subprocess.Popen([os.environ.get("CHROME_BROWSER_PATH"), '--remote-debugging-port=9222', '--user-data-dir={}'.format(os.environ.get("CHROME_USER_DATA_DIR"))])   # MAC
        # subprocess.Popen([os.environ.get("CHROME_BROWSER_PATH"), '--disable-dev-shm-usage', '--single-process', '--headless', '--no-sandbox', '--remote-debugging-port=9222', '--user-data-dir={}'.format(os.environ.get("CHROME_USER_DATA_DIR"))])   # Container
        # '--disable-gpu', 
        options = wd.ChromeOptions()
        # options.headless=True
        # options.add_argument("headless")
        # options.add_argument('--no-sandbox')
        # options.add_argument("--single-process")
        # options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("debuggerAddress", "0.0.0.0:9222")
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # subprocess.Popen([os.environ.get("CHROME_BROWSER_PATH"),'--remote-debugging-port=9222', '--user-data-dir="/Users/songdonghun/workspace/log/chrome_user_data"'])

        ### Chrome Debuger
        # subprocess
        
        ### Selenium webdriver
        # from selenium.webdriver.chrome.service import Service
        # from webdriver_manager.chrome import ChromeDriverManager
        # service = Service(executable_path=ChromeDriverManager().install())
        # service = Service(executable_path=os.environ.get("CHROME_EXCUTABLE_PATH"))
        # self.webdriver = Chrome(service=service, options=options)
        self.webdriver = webdriver if webdriver else wd.Chrome(executable_path=os.environ.get("CHROME_EXCUTABLE_PATH"), chrome_options=options)
        # self.webdriver = wd.Remote(command_executor="http://127.0.0.1:9222", options=options)

        ### Undetected_chrome webdriver
        # import undetected_chromedriver as uc
        # self.webdriver = webdriver if webdriver else uc.Chrome(service=service, options=options)
        # self.webdriver = webdriver if webdriver else uc.Chrome(driver_executable_path="/usr/bin/chromedriver", options=options)
        # self.webdriver = webdriver if webdriver else uc.Chrome(driver_executable_path="/srv/chromedriver", use_subprocess=True, options=options)
        # self.webdriver = webdriver if webdriver else uc.Chrome(browser_executable_path="/usr/bin/chromedriver", use_subprocess=True, options=options)

        ### Browser resize
        # self.webdriver.set_window_size(1200,900)
        # self.webdriver.set_window_position(0, 0)
        # self.webdriver.implicitly_wait(10)

        self.status_login = False

        print("ready to play")
        logging.info("ready to play")



    def login(self, method:str="google") -> bool:
        self.status_login = True    # Mutex

        self.webdriver.get('https://chat.openai.com/auth/login')
        self.webdriver.implicitly_wait(5)
        
        # Click Login
        try:
            self.webdriver.find_element(By.XPATH, '//button/div[text()="Log in"]').click()
            self.webdriver.implicitly_wait(5)
            
        except s_exception.NoSuchElementException:
            print("login page is something wrong.")
            logging.warning("login page is something wrong.")
            self.status_login = False
            return False


        # Login
        if method == "google":
            try:
                self.webdriver.find_element(By.XPATH, '//button/span[text()="Continue with Google"]').click()
                self.webdriver.implicitly_wait(5)
            except s_exception.NoSuchElementException:
                print("login option - google - is not found.")
                logging.warning("login option - google - is not found.")
                self.status_login = False
                return False
            else:
                self._login_google()
        # FIXME: MS 계정 로그인에대한 로직 구현
        elif method == "MS":
                self.webdriver.find_element(By.XPATH, '//button/span[text()="Continue with Microsoft Account"]').click()
                self.webdriver.implicitly_wait(5)
                self.status_login = False
                return False
        else:
            print("Not defined login method")
            logging.warning("Not defined login method")
            self.status_login = False
            return False

        print("[DONE] login successfully")
        logging.info("login successfully")
        self.status_login = True

        return True
    
    
    def _login_google(self):
        login_title = self.webdriver.find_element(By.XPATH, '//*[@id="headingText"]/span').text
        self.webdriver.implicitly_wait(5)

        if login_title == "계정 선택":
            # select use_other_account
            self.webdriver.find_element(By.XPATH, '//li[contains(div/div/div/text(),"다른 계정 사용")]').click()
            self.webdriver.implicitly_wait(5)
            # set id
            id = os.environ.get("GOOGLE_ID")
            self.webdriver.find_element(By.XPATH, '//input[contains(@type,"email")]').send_keys(id)
            self.webdriver.find_element(By.XPATH, '//button/span[text()="다음"]').click()
            self.webdriver.implicitly_wait(5)
            # set password
            pwd = os.environ.get("GOOGLE_PW")
            self.webdriver.find_element(By.XPATH, '//input[contains(@type,"password")]').send_keys(id)
            self.webdriver.find_element(By.XPATH, '//button/span[text()="다음"]').click()
            self.webdriver.implicitly_wait(5)

            ### TODO: 앞선코드 교체 > 계정 리스트 받아서 선택된 계정으로 로그인하는 과정 구현 필요
            # account_list = self.webdriver.find_elements(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li')
            # print("account_list = {}".format(account_list.count))

        elif login_title == "로그인":
            # set id
            id = os.environ.get("GOOGLE_ID")
            self.webdriver.find_element(By.XPATH, '//input[contains(@type,"email")]').send_keys(id)
            self.webdriver.find_element(By.XPATH, '//button/span[text()="다음"]').click()
            self.webdriver.implicitly_wait(5)
            # set password
            pwd = os.environ.get("GOOGLE_PW")
            self.webdriver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(pwd)
            self.webdriver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()
            self.webdriver.implicitly_wait(5)
        else:
            print("[ERROR] google login page is not expected from")
            logging.warning("google login page is not expected form")


    def skip_tutorial(self) -> bool:
        hasNext = True
        cnt = 0
        while hasNext:
            try:
                nextButton = self.webdriver.find_element(By.XPATH, '//button/div[text()="Next" or text()="Done"]')
                hasNext = (nextButton.text != "Done")
                nextButton.click()
                self.webdriver.implicitly_wait(5)
                cnt += 1
            except s_exception.NoSuchElementException:
                if cnt > 5:
                    print("[WARNING] Not found next button")
                    logging.warning("Not found next button")
                    return False

        print("skipped tutorial")
        logging.info("skipped tutorial")
        return True


    def send_message(self, message:str):
        self.webdriver.find_element(By.XPATH, '//textarea').send_keys(message)
        self.webdriver.find_element(By.XPATH, '//textarea/following-sibling::button').click()
        self.webdriver.implicitly_wait(5)

        response = ""
        waiting = True
        while waiting:
            
            try:
                request_button = self.webdriver.find_element(By.XPATH, '//textarea/following-sibling::button')
                self.webdriver.implicitly_wait(5)
                svg = request_button.find_element(By.TAG_NAME, 'svg')
                waiting = False if svg else True
                
                response_list = self.webdriver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/main/div[2]/div/div/div/div')
                self.webdriver.implicitly_wait(5)
                response = response_list[len(response_list)-2].text
                
                time.sleep(0.1)
            except s_exception.NoSuchElementException as nse:
                print("waiting response...")
                time.sleep(0.1)

        return response


    def new_chat(self, model:str=None) -> bool:

        try:
            new_chat_section = self.webdriver.find_element(By.XPATH, '//a[contains(text(),"New chat")]')
            new_chat_section.click()
            self.webdriver.implicitly_wait(5)

        except s_exception.NoSuchElementException as nse:
            logging.warning("Not found new_chat section")
            print("Not found new_chat section")
            return False

        if model:
            self.set_model(modelName=model)

        return True


    def set_model(self, modelName:str=None) -> bool:
        """
        GPT 질의 전 상단의 모델 선택을 위해 사용
        PARAM. modelName : (Default | GPT-4)
        """
        # check Param
        if not modelName or (modelName not in ["GPT-4", "Default"]):
            modelName = "Default"
    
        # open modelListBox
        try:
            self.webdriver.find_element(By.XPATH, '//label[text()="Model"]/parent::button').click()
            self.webdriver.implicitly_wait(5)
        except s_exception.NoSuchElementException as nse:
            logging.warning("Not found model list box")
            print("Not found model list box")
            return False

        # select model
        self.webdriver.find_element(By.XPATH, '//label[text()="Model"]/parent::button/following-sibling::div')
        modelList = self.webdriver.find_elements(By.XPATH, '//label[text()="Model"]/parent::button/following-sibling::div/ul/li')
        self.webdriver.implicitly_wait(5)
        for eachModel in modelList:
            if modelName in eachModel.text:
                eachModel.click()
                break
        else:
            print("Not found maching model - {}".format(modelName))
            logging.warning("Not found maching model - {}".format(modelName))
            return False
        
        return True