#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

USERNAME = 'admin'
PASSWORD = 'admin'

class RestartRouter:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    def wait_to_load(self, id: str, by_type = By.ID):
        print(f"Waiting.. {(by_type, id)}")
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((by_type, id)))
        print("Done.")

    def load_page(self, url: str):
        print(f"Waiting for page to load: {url}")
        self.driver.get(url)
        print("Done")

    def wait_and_fill(self, id: str, value):
        try:
            dom = None
            while not dom:
                print(f"Looking for {id}...")
                wait = WebDriverWait(self.driver, 20)
                dom = wait.until(
                    EC.presence_of_element_located((By.ID, id))
                )
            dom.send_keys(value)
            print(f"{id}: Done")
        except Exception as e:
            print(e)
            print(self.driver.page_source)
            exit(1)

    def click_button(self, id: str):
        print(f"Click button {id}")
        button = self.driver.find_element_by_id(id)
        button.click()
        print("Done.")

    def run(self):
        # Do login

        ## Force twice since they can redirect us in the first try
        self.load_page('http://192.168.15.1/webClient/login.html')
        self.wait_to_load('header-gateway')
        time.sleep(1)
        self.load_page('http://192.168.15.1/webClient/login.html')
        self.wait_to_load('header-gateway')

        self.wait_and_fill("txtUser", USERNAME)
        self.wait_and_fill("txtPass", PASSWORD)
        self.click_button('btnLogin')

        # Restart
        self.load_page('http://192.168.15.1/webClient/popup-reboot.html')
        self.wait_to_load('no-bg', by_type=By.CLASS_NAME)
        self.driver.execute_script("btnaAccept()")

        # Close
        self.driver.close()

if __name__ == '__main__':
    restart_router = RestartRouter()
    restart_router.run()
