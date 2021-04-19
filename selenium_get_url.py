from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class Judge:
    def __call__(self, driver):
        node = driver.find_element_by_xpath('//*[@id="viewFrame"]')
        if 'm3u8' in node.get_attribute('src'):
            return node.get_attribute('src')
        else:
            return False


class InitDriver:
    def __init__(self,path,url):
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.get(url)

    def get_url(self):
        element = WebDriverWait(self.driver, 30).until(Judge())
        self.driver.quit()
        return element
