from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os


class ParsAT:

    def __init__(self, url, login='', password='', name='data' ):


        self.log = login
        self.password = password
        self.url = url
        self.name = name
        self.driver = webdriver.Chrome(executable_path="chromedriver")
        self.text = ''
        self.state = 'ok'
        self.pars = True
        self.cur_chapter = 'Начали'
        self.error = 'Default'

    def login(self):
        self.driver.get('https://author.today/')
        log_in = self.driver.find_element(By.ID, 'navbar-right')
        log_in.click()

        sleep(1)

        self.driver.find_element(By.CLASS_NAME, 'modal-body').find_element(By.NAME, 'Login').send_keys(self.log)
        self.driver.find_element(By.CLASS_NAME, 'modal-body').find_element(By.NAME, 'Password').send_keys(self.password)
        self.driver.find_element(By.CLASS_NAME, 'modal-body').find_element(By.CLASS_NAME, 'btn-primary').click()
        sleep(2)

        err = self.driver.find_element(By.CLASS_NAME, 'modal-body').find_element(By.CLASS_NAME, 'error-messages')

        if err.text:
            print(err.text)
            self.state = 'err'
            self.error = err.text
            self.pars = False
            self.driver.close()

        else:
            self.cur_chapter = 'Аутентификация прошла успешно'
            self.get_text()

    def get_text(self):

        if 'reader' not in self.url:
            num = self.url.split('/')[-1]
            self.url = 'https://author.today/reader/' + num

        self.driver.get(self.url)

        try:
            text = self.driver.find_element(By.ID, 'text-container').text

            while True:
                try:
                    sleep(2)
                    self.text += ' ' + self.driver.find_element(By.ID, 'text-container').text
                    btn = self.driver.find_element(By.CLASS_NAME, 'next').find_element(By.TAG_NAME, 'a')
                    print(btn.text)
                    self.cur_chapter = btn.text
                    btn.click()
                except:
                    print('Страницы кончились')
                    break

            self.save_text()
            self.driver.close()
            self.pars = False

        except:
            err = self.driver.find_element(By.TAG_NAME, 'h1')

            self.state = 'err'
            self.error = err.text
            self.driver.close()
            self.pars = False
            print(self.error)

    def save_text(self):
        with open(f'{self.name}.txt', 'w', encoding='utf-8') as f:
            f.write(self.text)


if __name__ == '__main__':
    pars = ParsAT('https://author.today/work/82394', 'aisavikin@gmail.com', 'eto2016Detk*', '123')
    pars.login()
    print(pars.text)
