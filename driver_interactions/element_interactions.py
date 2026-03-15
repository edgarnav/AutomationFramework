import time
from traceback import print_stack
from allure_commons.types import AttachmentType
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import utilities.constants as constants
import utilities.logger as log
import allure


class ElementInteractions:
    log = log.func_logger()

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def launch_web_page(self, url):
        try:
            self.webdriver.get(url)
            self.log.info(constants.web_page_launched + url)
        except Exception:
            self.log.info(constants.not_web_page_launched + url)

    def verify_page(self, page_name):
        if page_name != self.webdriver.title:
            self.take_screenshot(self.webdriver.title)
            assert False

    def back_page(self):
        self.webdriver.back()

    def explicit_wait(self, locator_value, locator_by_type, time):
        try:
            WebDriverWait(self.webdriver, time).until(
                ec.presence_of_all_elements_located((locator_by_type, locator_value)))
            self.log.info(constants.found_locator + locator_value + constants.locator_type + locator_by_type)
        except Exception:
            self.log.error(
                constants.not_found_locator + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def get_element(self, locator_value, locator_by_type):
        element = None
        try:
            element = self.webdriver.find_element(locator_by_type, locator_value)
            self.log.info(constants.found_locator + locator_value + constants.locator_type + locator_by_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                constants.not_found_locator + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
        return element

    def get_all_elements(self, locator_value, locator_by_type):
        elements = None
        try:
            self.wait_element(locator_value, locator_by_type)
            elements = self.webdriver.find_elements(locator_by_type, locator_value)
            self.log.info(constants.found_locator + locator_value + constants.locator_type + locator_by_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                constants.not_found_locator + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
        return elements

    def wait_element(self, locator_value, locator_by_type):
        try:
            wait = WebDriverWait(self.webdriver, 25, poll_frequency=1,
                                 ignored_exceptions=[ElementNotVisibleException, NoSuchElementException])
            element = wait.until(ec.presence_of_element_located((locator_by_type, locator_value)))
            self.log.info(constants.found_locator + locator_value + constants.locator_type + locator_by_type)
        except Exception:
            self.log.error(
                constants.not_found_locator + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False
        return element

    def press_element(self, locator_value, locator_by_type):
        try:
            element = self.wait_element(locator_value, locator_by_type)
            element.click()
            self.log.info(constants.clicked_element + locator_value + constants.locator_type + locator_by_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(constants.not_clicked_element + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def send_text(self, text, locator_value, locator_by_type):
        try:
            element = self.wait_element(locator_value, locator_by_type)
            element.clear()
            element.send_keys(text)
            self.log.info(
                "Sent the text " + text + " in element with locator value " + locator_value + constants.locator_type + locator_by_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                "Unable to sent the text " + text + " in element with locator value " + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def get_text(self, locator_value, locator_type):
        element_text = None
        try:
            element = self.wait_element(locator_value, locator_type)
            element_text = element.text
            self.log.info(
                "Got the text " + element_text + " from element with locator value " + locator_value + constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(
                "Unable to get the text " + element_text + " from element with locator value " + locator_value + constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
        return element_text

    def select_by_value(self, locator_value, locator_type, value):
        try:
            element = self.wait_element(locator_value, locator_type)
            Select(element).select_by_value(value)
            self.log.info(constants.element_selected + locator_value + constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
        except Exception:
            self.log.error(constants.not_element_selected + locator_value + constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def is_element_displayed(self, locator_value, locator_by_type):
        try:
            element = self.wait_element(locator_value, locator_by_type)
            element_displayed = element.is_displayed()
            self.take_screenshot(locator_value)
            self.log.info(constants.element_displayed + locator_value + constants.locator_type + locator_by_type)
            return element_displayed
        except Exception:
            self.log.error(constants.not_element_displayed + locator_value + constants.locator_type + locator_by_type)
            print_stack()
            self.take_screenshot(locator_value)
            assert False

    def scroll_to_element(self, locator_value, locator_type):
        try:
            element = self.wait_element(locator_value, locator_type)
            actions = ActionChains(self.webdriver)
            actions.move_to_element(element).perform()
            self.log.info(constants.element_found_scrolling + locator_value + constants.locator_type + locator_type)
            self.take_screenshot(locator_value)
            return True
        except Exception:
            self.log.error(constants.not_element_found_scrolling + locator_value + constants.locator_type + locator_type)
            print_stack()
            self.take_screenshot(locator_value)
            return False

    def hover_element(self, element):
        try:
            actions = ActionChains(self.webdriver)
            actions.move_to_element(element).perform()
            self.log.info(constants.hover_element)
            self.take_screenshot(constants.hover_element)
        except Exception:
            self.log.error(constants.not_element_displayed)
            print_stack()
            self.take_screenshot(constants.not_element_displayed)

    def get_html(self):
        try:
            page = self.webdriver.page_source
            return page
        except Exception:
            self.log.info(constants.not_web_page_launched)
            assert False

    def perform_enter(self):
        actions = ActionChains(self.webdriver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def take_screenshot(self, text):
        allure.attach(self.webdriver.get_screenshot_as_png(), name=text, attachment_type=AttachmentType.PNG)
