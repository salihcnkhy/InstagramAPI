from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, Response
import requests

#options = Options()
#options.add_argument("--headless")
#_driver = webdriver.Chrome('./chromedriver', options=options)


class InstagramSelenium:
    class LoginPageXPaths(Enum):
        usernameField = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input"
        passwordField = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input"
        nonCorrectPassword = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[7]"

    class TwoFactorPageFields(Enum):
        codeField = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input"
        confirmButton = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[2]/button"
        nonCorrectCode = "//*[@id='react-root']/section/main/div/article/div/div[1]/div/div[2]"

    class URLs(Enum):
        LoginPage = "https://www.instagram.com/accounts/login/"

    _driver = webdriver.Chrome('./chromedriver')

    def waitForElementsLoad(self, timeout, waitingElements):
        for element in waitingElements:
            try:
                WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, element)))
            except TimeoutException:
                return False
        return True

    def signIn(self, username, password):

        self._driver.get(self.URLs.LoginPage.value)

        self.waitForElementsLoad(20,
                                 [self.LoginPageXPaths.usernameField.value, self.LoginPageXPaths.passwordField.value])

        usernameInput = self._driver.find_element_by_xpath(self.LoginPageXPaths.usernameField.value)
        passwordInput = self._driver.find_element_by_xpath(self.LoginPageXPaths.passwordField.value)

        usernameInput.send_keys(username)
        passwordInput.send_keys(password)
        passwordInput.send_keys(Keys.ENTER)

        if self.waitForElementsLoad(5, [self.LoginPageXPaths.nonCorrectPassword.value]):
            return "nonCorrect"
        if self.waitForElementsLoad(5, [self.TwoFactorPageFields.codeField.value]):
            return "twoFactor"

        return "TimeOut"

    def waitPageLoadedTo(self):

        previousUrl = self._driver.current_url
        try:
            WebDriverWait(self._driver, 10).until(lambda d: d.current_url != previousUrl)
            return True
        except TimeoutException:
            return False

    def enterTwoFactor(self, code):

        if self.waitForElementsLoad(5, [self.TwoFactorPageFields.codeField.value,
                                        self.TwoFactorPageFields.confirmButton.value]):
            codeField = self._driver.find_element_by_xpath(self.TwoFactorPageFields.codeField.value)
            confirmButton = self._driver.find_element_by_xpath(self.TwoFactorPageFields.confirmButton.value)

            codeField.clear()
            codeField.send_keys(code)
            confirmButton.click()

            if self.waitPageLoadedTo():
                return "Success"
            if self.waitForElementsLoad(7, [self.TwoFactorPageFields.nonCorrectCode.value]):
                return "nonCorrect"

            return "TimeOut"

    def getFollowerList(self):

        self._driver.get(f"https://www.instagram.com/{self.username}")
        followersBtn = self._driver.find_element_by_xpath()


app = Flask(__name__)
instAPI = InstagramSelenium()


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        responseFromSelenium = instAPI.signIn(attempted_username, attempted_password)
        print(responseFromSelenium)
        if responseFromSelenium == "TwoFactor":
            return Response(status=202)  # 202 means need two factor code
        else:
            return Response(status=200)  # 200 means success to login


@app.route('/loginTwo', methods=["POST"])
def twoFactor():
    if request.method == "POST":
        attempted_code = request.form['code']
        instAPI.enterTwoFactor(attempted_code)

        return Response(status=200)


if __name__ == '__main__':
    app.run(port=5000)
