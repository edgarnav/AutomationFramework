import subprocess


def run_behave(test_target, log_view, report):
    command = f"behave --tags={test_target}"
    try:
        if log_view:
            cmd = f"{command} -f plain"
            subprocess.run(cmd, shell=True, check=True)
        else:
            cmd = f"{command} -f allure_behave.formatter:AllureFormatter -o {report}"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(f"Ended process regarding to {test_target}: {stderr.decode('utf-8')}")
            subprocess.run(f"allure serve {report}", shell=True, check=True)
    except Exception as error:
        print(f"An exception has occurred in the execution {test_target}: {str(error)}")


if __name__ == '__main__':
    log = True
    run_behave("regression", False, "reports")
