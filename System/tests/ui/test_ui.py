from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class DomainLegitimacyCheckerUITest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_home_page(self):
        driver = self.driver
        driver.get("http://localhost:5000")
        self.assertIn("Domain Legitimacy Checker", driver.title)
        elem = driver.find_element_by_id("domain")
        elem.send_keys("example.com")
        elem.send_keys(Keys.RETURN)
        self.assertIn("Analysis Results", driver.page_source)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
