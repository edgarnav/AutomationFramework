from pip._internal.exceptions import ConfigurationError
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver as selenium_driver
from appium import webdriver as appium_driver
import configurations as configurations
import utilities.capabilities as capabilities


class InitWebDriver:

    @staticmethod
    def init_driver(testcase_id, testcase_name):
        if configurations.platform.lower() == "web":
            if configurations.browser.lower() == "chrome":
                return InitWebDriver.init_chrome_driver()
            elif configurations.browser.lower() == "firefox":
                return InitWebDriver.init_firefox_driver()
            else:
                raise ConfigurationError(f"Unsupported browser type: {configurations.browser}")
        elif configurations.platform.lower() in ['android', 'ios', 'windows']:
            return InitWebDriver.init_appium_driver(testcase_id, testcase_name)
        else:
            assert False

    @staticmethod
    def init_chrome_driver():
        options = ChromeOptions()
        if configurations.hide_browser:
            options.add_argument('--headless=new')
        options.add_argument('--disable-blink-features=AutomationControlled')
        driver = selenium_driver.Chrome(options=options)
        driver.get(configurations.website_app_url)
        driver.maximize_window()
        return driver

    @staticmethod
    def init_firefox_driver():
        options = FirefoxOptions()
        if configurations.hide_browser:
            options.add_argument('--headless=new')
        driver = selenium_driver.Firefox(options=options)
        driver.get(configurations.website_app_url)
        driver.maximize_window()
        return driver

    @staticmethod
    def init_appium_driver(testcase_id, testcase_name):
        if configurations.platform.lower() == "ios":
            options = capabilities.get_ios_capabilities(testcase_id, testcase_name)
        elif configurations.platform.lower() == "android":
            options = capabilities.get_android_capabilities(testcase_id, testcase_name)
        else:
            options = capabilities.get_windows_capabilities()
        try:
            driver = appium_driver.Remote(
                command_executor=configurations.appium_server_url,
                options=options
            )
            return driver
        except Exception:
            return False
