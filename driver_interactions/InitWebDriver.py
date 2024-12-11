from pip._internal.exceptions import ConfigurationError
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import configurations.ConfigFile as Configs


class InitWebDriver:

    @staticmethod
    def init_web_driver():
        if Configs.browser.lower() == 'chrome':
            return InitWebDriver.init_chrome_driver()
        elif Configs.browser.lower() == 'firefox':
            return InitWebDriver.init_firefox_driver()
        else:
            raise ConfigurationError(f"Unsupported browser type: {Configs.browser}")

    @staticmethod
    def init_chrome_driver():
        options = ChromeOptions()
        if Configs.hidden_view:
            options.add_argument('--headless=new')
        options.add_argument('--disable-blink-features=AutomationControlled')
        web_driver = webdriver.Chrome(options=options)
        web_driver.maximize_window()
        return web_driver

    @staticmethod
    def init_firefox_driver():
        options = FirefoxOptions()
        if Configs.hidden_view:
            options.add_argument('--headless=new')
        web_driver = webdriver.Firefox(options=options)
        web_driver.maximize_window()
        return web_driver
