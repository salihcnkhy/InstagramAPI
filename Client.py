from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, Response

import requests


class InstagramSelenium:

    username = ""
    password = ""

    class ProfiilePageXPaths(Enum):
        followersBtn = ""
        followingBtn = ""

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
        MainPage = "https://www.instagram.com/"

    _driver = webdriver.Chrome('./chromedriver')

    def waitForElementsLoad(self, timeout, waitingElements):
        for element in waitingElements:
            try:
                WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, element)))
            except TimeoutException:
                return False
        return True

    def _loadPage(self,URL):
        self._driver.get(URL)

    def signIn(self, username, password):
        self.username = username
        self.password = password
        self._loadPage(self.URLs.LoginPage.value)

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

       self._loadPage(self.URLs.MainPage.value+self.username)



if __name__ == '__main__':
    instAPI = InstagramSelenium()
    responseFromSelenium = instAPI.signIn("salihcnkhy", 'dyNsim-1siQhy-0byhXa')
    if responseFromSelenium == "twoFactor":
        code = input()
        text = instAPI.enterTwoFactor(code)
        print(text)
        while str(text) == "nonCorrect":
            code = input()
            text = instAPI.enterTwoFactor(code)
            print(text)

    # userInfo = {'username': 'salihcnkhy' , 'password':'dyNsim-1siQhy-0byhXa'}
    # x = requests.post("http://127.0.0.1:5000/login",data=userInfo)
    # if x.status_code == 202:
    #     inputCode = input()
    #     loginCode = {'code' : inputCode}
    #     x = requests.post("http://127.0.0.1:5000/loginTwo",data=loginCode)
    #     print(x.status_code)
