from appium.options.android import UiAutomator2Options
import configurations as configurations
import unicodedata
import os


def get_ios_capabilities(testcase_id, testcase_name):

    options = UiAutomator2Options()
    options.platform_name = configurations.platform
    options.automation_name = "XCUITest"
    options.set_capability("appium:deviceName", ".*")
    options.app = f"storage:{configurations.application_name}"
    options.auto_grant_permissions = True
    sauce_options = {
        "username":  os.environ.get("SAUCE_USERNAME"),
        "accessKey": os.environ.get("SAUCE_ACCESS_KEY"),
        "name": f"{testcase_id}: {remove_accents(testcase_name)}",
        "phoneOnly": True,
    }
    options.set_capability("sauce:options", sauce_options)
    return options


def get_android_capabilities(testcase_id, testcase_name):

    options = UiAutomator2Options()
    options.platform_name = configurations.platform
    options.automation_name = "UiAutomator2"
    options.app = f"storage:{configurations.application_name}"
    options.auto_grant_permissions = True
    sauce_options = {
        "username":  os.environ.get("SAUCE_USERNAME"),
        "accessKey": os.environ.get("SAUCE_ACCESS_KEY"),
        "name": f"{testcase_id}: {remove_accents(testcase_name)}",
        "phoneOnly": True,
        "appiumVersion": "latest"
    }
    options.set_capability("sauce:options", sauce_options)
    options.set_capability("appium:deviceName", ".*")
    options.set_capability("chromedriverAutodownload", True)
    options.set_capability("appium:goog:chromeOptions", {"w3c": False})

    return options


def get_windows_capabilities():

    caps = {
        "platformName": "Windows",
        "appium:automationName": "windows",
        "appium:app": configurations.windows_application_path_exe,
        "appium:deviceName": "WindowsPC",
        "appium:newCommandTimeout": 3600
    }
    return caps


def remove_accents(text):

    normalize_text = unicodedata.normalize('NFD', text)

    final_text = "".join(
        c for c in normalize_text
        if unicodedata.category(c) != 'Mn'
    )

    return final_text
