matrix_testcases_path = ""  # Include the filename.xlsx
path_saved_testcases = ""  # Folder name where the automated testcases will be saved them
# Define the platform where you will perform the testcases
platform = ""  # web, android, ios, mobile_web, windows
# Web application
website_app_url = ""  # URL of the web application to test
browser = ""  # chrome, firefox
hide_browser = True  # Keep it True if you don't want to see the execution in browser or to perform the tests in CI/CD
# Mobile applications
appium_server_url = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"  # URL appium server, leave empty for windows platform
windows_application_path_exe = ""  # path/tp/application.exe
# Remove filename= if you will add an ID or add it if you will add the app_name.apk (filename=app_name.ipa) or (5f585002-751d-4b8d-ba95-097cb8d0e84d)
application_name = ""  # Name of the mobile application to test app.ipa / app.aab / app.apk,
