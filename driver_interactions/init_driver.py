from pip._internal.exceptions import ConfigurationError
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver as selenium_driver
from appium import webdriver as appium_driver
from appium.options.common import AppiumOptions
import configurations.configurations as configurations
import configurations.capabilities as capabilities


class InitWebDriver:

    @staticmethod
    def init_driver(testcase):
        if configurations.platform == "web":
            if configurations.browser.lower() == "chrome":
                return InitWebDriver.init_chrome_driver()
            elif configurations.browser.lower() == "firefox":
                return InitWebDriver.init_firefox_driver()
            else:
                raise ConfigurationError(f"Unsupported browser type: {configurations.browser}")
        elif configurations.platform == "mobile_native":
            return InitWebDriver.init_appium_driver(testcase)
        else:
            assert False

    @staticmethod
    def init_chrome_driver():
        options = ChromeOptions()
        if configurations.hide_browser:
            options.add_argument('--headless=new')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = selenium_driver.Chrome(options=options)
        driver.maximize_window()
        return driver

    @staticmethod
    def init_firefox_driver():
        options = FirefoxOptions()
        if configurations.hide_browser:
            options.add_argument('--headless=new')
        driver = selenium_driver.Firefox(options=options)
        driver.maximize_window()
        return driver

    @staticmethod
    def init_appium_driver(test_case):
        if configurations.platform == "ios":
            caps = capabilities.get_ios_capabilities(test_case['id'], test_case['name'])
        else:
            caps = capabilities.get_android_capabilities(test_case['id'], test_case['name'])
        options = AppiumOptions().load_capabilities(caps)
        driver = appium_driver.Remote(
            command_executor=configurations.appium_server_url,
            options=options
        )
        return driver
