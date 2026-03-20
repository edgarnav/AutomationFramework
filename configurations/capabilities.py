import configurations.configurations as configurations
import os


def get_ios_capabilities(test_id, test_name):

    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:deviceName": "iPhone .* ",
        "appium:platformVersion": configurations.mobile_platformVersion,
        "appium:app": "storage:filename=app.ipa",

        "sauce:options": {
            "username": os.environ.get("SAUCE_USERNAME"),
            "accessKey": os.environ.get("SAUCE_ACCESS_KEY"),
            "build": "Build-AI-Framework-001",
            "name": f"{test_id}: {test_name}",
            "deviceOrientation": "portrait"
        }
    }
    return caps


def get_android_capabilities(test_id, test_name):

    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "Google Pixel .*|Samsung Galaxy .*",
        "appium:platformVersion": configurations.mobile_platformVersion,
        "appium:app": "storage:filename=mi_app_coppel.apk",

        "appium:appPackage": "com.coppel.android",
        "appium:appWaitActivity": "com.coppel.android.MainActivity",

        "sauce:options": {
            "username": os.environ.get("SAUCE_USERNAME"),
            "accessKey": os.environ.get("SAUCE_ACCESS_KEY"),
            "build": "Build-Android-AI-001",
            "name": f"{test_id}: {test_name}",
            "deviceOrientation": "portrait"
        }
    }
    return caps


def get_windows_capabilities():

    caps = {
        "platformName": "Windows",
        "appium:automationName": "windows",
        "appium:app": configurations.windows_application_path_exe,
        "appium:deviceName": "WindowsPC",
        "appium:newCommandTimeout": 3600
    }
    return caps
