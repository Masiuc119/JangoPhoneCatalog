import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PhoneCatalogTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_login_logout(self):
        s = 0  # время пауз
        for i in range(5):
            driver = self.driver
            driver.get("http://127.0.0.1:8000/PhoneCatalog/")
            time.sleep(s)
            elem = driver.find_element_by_link_text("Log in")
            elem.click()
            time.sleep(s)
            elem = driver.find_element_by_xpath("//input[@name='username']")
            elem.send_keys("Admin")
            elem = driver.find_element_by_xpath("//input[@name='password']")
            elem.send_keys("AdMiN")
            elem.send_keys(Keys.RETURN)
            time.sleep(s)
            self.assertIn("Hello,", driver.page_source)
            time.sleep(s)
            print(driver.page_source)
            elem = driver.find_element_by_link_text("Log out")
            elem.click()
            time.sleep(s)
            self.assertNotIn("Log out", driver.page_source)
            i += 1


if __name__ == '__main__':
    unittest.main()
