matrix_testcases_path = "TestAIFramework.xlsx"  # Include the filename.xlsx
path_saved_testcases = "saved_testcases"  # Folder name where the automated testcases will be saved them
# Define the platform where you will perform the testcases
platform = "web"  # web, android, ios, mobile_web, windows
# Web application
website = "https://practicetestautomation.com/practice-test-login/"
browser = "chrome"  # chrome, firefox
hide_browser = True
# Mobile applications
appium_server_url = ""  # URL appium server, leave empty for windows platform
mobile_platformVersion = ""  # Specify the OS version for mobile android or ios
windows_application_path_exe = ""  # path/tp/application.exe
