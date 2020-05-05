from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class InstagramAPI:
    username = ""
    pasword = ""
    _driver = webdriver.Chrome('./chromedriver')

    # options = Options()
    # options.add_argument("--headless")

    def setEmailAndPassword(self, username, password):
        self.username = username
        self.password = password

    def signIn(self):
        loginURL = "https://www.instagram.com/accounts/login/"

        emailFieldXpath = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input"
        passwordFieldXpath = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input"

        self._driver.get(loginURL)

        try:
            element = EC.presence_of_element_located((By.XPATH, emailFieldXpath))
            WebDriverWait(self._driver, 10).until(element)
        except TimeoutException:
            print("timeOut")
        emailInput = self._driver.find_element_by_xpath(emailFieldXpath)
        passwordInput = self._driver.find_element_by_xpath(passwordFieldXpath)

        emailInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        try:
            twoFactorXPath = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input"
            twoFactor = EC.presence_of_element_located((By.XPATH, twoFactorXPath))
            WebDriverWait(self._driver, 7).until(twoFactor)
            return "TwoFactor"
        except TimeoutException:
            print("giriş Başarılı")
            return "Success"

    def getFollowerList(self):

        self._driver.get(f"https://www.instagram.com/{self.username}")
        followersBtn = self._driver.find_element_by_xpath()

    def enterTwoFactor(self, code):
        inputXPath = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input"
        confirmButtonXPath = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/button"
        confirmBtn = self._driver.find_element_by_xpath(confirmButtonXPath)
        codeInput = self._driver.find_element_by_xpath(inputXPath)
        print(code)
        codeInput.send_keys(code)
        confirmBtn.click()
        time.sleep(10)

instagramAPI = InstagramAPI()

instagramAPI.setEmailAndPassword("xxxxx", "yyyyyyy")
if (instagramAPI.signIn() == "TwoFactor"):
    input = str(input())
    instagramAPI.enterTwoFactor(input)

