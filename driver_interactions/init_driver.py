from pip._internal.exceptions import ConfigurationError
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import configurations.configurations as configurations


class InitWebDriver:

    @staticmethod
    def init_driver():
        if configurations.browser.lower() == 'chrome':
            return InitWebDriver.init_chrome_driver()
        elif configurations.browser.lower() == 'firefox':
            return InitWebDriver.init_firefox_driver()
        else:
            raise ConfigurationError(f"Unsupported browser type: {configurations.browser}")

    @staticmethod
    def init_chrome_driver():
        options = ChromeOptions()
        if configurations.hidden_view:
            options.add_argument('--headless=new')
        options.add_argument('--disable-blink-features=AutomationControlled')
        web_driver = webdriver.Chrome(options=options)
        web_driver.maximize_window()
        return web_driver

    @staticmethod
    def init_firefox_driver():
        options = FirefoxOptions()
        if configurations.hidden_view:
            options.add_argument('--headless=new')
        web_driver = webdriver.Firefox(options=options)
        web_driver.maximize_window()
        return web_driver
