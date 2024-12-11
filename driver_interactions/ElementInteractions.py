from traceback import print_stack
from allure_commons.types import AttachmentType
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import utilities.Constants as Constants
import utilities.Logger as Log
import allure


class ElementInteractions:
    log = Log.func_logger()

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def locator(self, locator_type):
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "tag":
            return By.TAG_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "plink":
            return By.PARTIAL_LINK_TEXT
        else:
            self.log.error("Locator Type : " + locator_type + " entered is not found")
        return False

    def launch_web_page(self, url):
        try:
            self.webdriver.get(url)
            self.log.info(Constants.web_page_launched + url)
        except Exception:
            self.log.info(Constants.not_web_page_launched + url)

    def go_to_url(self, url):
        self.webdriver.get(url)

    def verify_page(self, page_name):
        if page_name != self.webdriver.title:
            self.take_screenshot(self.webdriver.title)
            assert False

    def back_page(self):
        self.webdriver.back()

    def explicit_wait(self, locator_value, locator_type, time):
        try:
            locator_by_type = self.locator(locator_type)
            WebDriverWait(self.webdriver, time).until(
                ec.presence_of_all_elements_located((locator_by_type, locator_value)))
            self.log.info(Constants.found_locator + locator_value + Constants.locator_type + locator_by_type)
        except Exception:
            self.log.error(
                Constants.not_found_locator + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def get_element(self, locator_value, locator_type):
        element = None
        try:
            locator_by_type = self.locator(locator_type)
            element = self.webdriver.find_element(locator_by_type, locator_value)
            self.log.info(Constants.found_locator + locator_value + Constants.locator_type + locator_by_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                Constants.not_found_locator + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
        return element

    def get_all_elements(self, locator_value, locator_type):
        elements = None
        try:
            locator_by_type = self.locator(locator_type)
            elements = self.webdriver.find_elements(locator_by_type, locator_value)
            self.log.info(Constants.found_locator + locator_value + Constants.locator_type + locator_by_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                Constants.not_found_locator + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
        return elements

    def wait_element(self, locator_value, locator_type):
        try:
            locator_by_type = self.locator(locator_type)
            wait = WebDriverWait(self.webdriver, 25, poll_frequency=1,
                                 ignored_exceptions=[ElementNotVisibleException, NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((locator_by_type, locator_value)))
            self.log.info(Constants.found_locator + locator_value + Constants.locator_type + locator_type)
        except Exception:
            self.log.error(
                Constants.not_found_locator + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False
        return element

    def press_element(self, locator_value, locator_type):
        try:
            element = self.wait_element(locator_value, locator_type)
            element.click()
            self.log.info(Constants.clicked_element + locator_value + Constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(Constants.not_clicked_element + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def send_text(self, text, locator_value, locator_type):
        try:
            element = self.wait_element(locator_value, locator_type)
            element.send_keys(text)
            self.log.info(
                "Sent the text " + text + " in element with locator value " + locator_value + Constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                "Unable to sent the text " + text + " in element with locator value " + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def get_text(self, locator_value, locator_type):
        element_text = None
        try:
            element = self.wait_element(locator_value, locator_type)
            element_text = element.text
            self.log.info(
                "Got the text " + element_text + " from element with locator value " + locator_value + Constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                "Unable to get the text " + element_text + " from element with locator value " + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
        return element_text

    def select_by_value(self, locator_value, locator_type, value):
        try:
            element = self.wait_element(locator_value, locator_type)
            Select(element).select_by_value(value)
            self.log.info(Constants.element_selected + locator_value + Constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(Constants.not_element_selected + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def is_element_displayed(self, locator_value, locator_type):
        try:
            element = self.wait_element(locator_value, locator_type)
            element_displayed = element.is_displayed()
            self.take_screenshot(locator_value)
            self.log.info(Constants.element_displayed + locator_value + Constants.locator_type + locator_type)
            return element_displayed
        except Exception:
            self.log.error(Constants.not_element_displayed + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def scroll_to_element(self, locator_value, locator_type):
        try:
            element = self.wait_element(locator_value, locator_type)
            actions = ActionChains(self.webdriver)
            actions.move_to_element(element).perform()
            self.log.info(Constants.element_found_scrolling + locator_value + Constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
            return True
        except Exception:
            self.log.error(Constants.not_element_found_scrolling + locator_value + Constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            return False

    def hover_element(self, element):
        try:
            actions = ActionChains(self.webdriver)
            actions.move_to_element(element).perform()
            self.log.info(Constants.hover_element)
            self.take_screenshot(Constants.hover_element)
        except Exception:
            self.log.error(Constants.not_element_displayed)
            print_stack()
            self.take_screenshot(Constants.not_element_displayed)

    def perform_enter(self):
        actions = ActionChains(self.webdriver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def take_screenshot(self, text):
        allure.attach(self.webdriver.get_screenshot_as_png(), name=text, attachment_type=AttachmentType.PNG)
