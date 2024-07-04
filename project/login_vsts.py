from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginVSTS:
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 5)
 
    def _init_(self):
        self.browser = self.browser
        self.wait = self.wait
 
 
    def Authentication(self):
        mail = input('Digite seu e-mail: ')
        password = input('Digite sua senha: ')
        self.browser.maximize_window()
        self.browser.get('https://dev.azure.com/ONR-SAEC/ONR.Sustentacao/_boards/board/t/ONR.Sustentacao%20Team/Backlog%20items')
        self.browser.implicitly_wait(100)
 
        # Realizando o login
 
        # Mail
        self.browser.find_element(By.XPATH, '//input[@id="i0116"]').send_keys(mail)
        self.browser.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
 
        # Password
        self.wait.until(EC.presence_of_element_located((By.ID, "idA_PWD_ForgotPassword")))
        self.browser.find_element(By.XPATH, '//input[@id="i0118"]').send_keys(password)
        self.browser.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
 
        # Stay connected
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="row text-title"]')))
        self.browser.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
