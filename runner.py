import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


# URL por defecto donde corre WinAppDriver
WINAPPDRIVER_URL = 'http://127.0.0.1:4723'

# El Application ID de la Calculadora de Windows (moderna)
# Se encuentra en el formato PackageFamilyName!ApplicationId
CALCULATOR_APP_ID = 'Microsoft.WindowsCalculator_8wekyb3d8bbwe!App'


def test_suma_calculadora():
    # Desired Capabilities para WinAppDriver
    # Se especifica la plataforma, el nombre de la aplicación y la ruta del driver
    desired_caps = {}
    desired_caps["app"] = CALCULATOR_APP_ID
    desired_caps["platformName"] = "Windows"
    desired_caps["deviceName"] = "WindowsPC"

    # 1. Conectar al servicio de WinAppDriver
    print("Iniciando conexión con WinAppDriver...")
    driver = webdriver.Remote(
        command_executor=WINAPPDRIVER_URL,
        desired_capabilities=desired_caps
    )

    try:
        # Esperar hasta que la ventana principal de la Calculadora esté visible
        wait = WebDriverWait(driver, 10)

        # 2. Localizar elementos por su Automation ID
        # NOTA: En WinAppDriver se usa By.NAME o By.ACCESSIBILITY_ID (que mapea a Automation ID)

        btn_seven = wait.until(EC.presence_of_element_located((By.NAME, "Siete")))
        btn_plus = wait.until(EC.presence_of_element_located((By.NAME, "Más")))
        btn_three = wait.until(EC.presence_of_element_located((By.NAME, "Tres")))
        btn_equal = wait.until(EC.presence_of_element_located((By.NAME, "Igual")))

        # El campo de resultado también puede ser localizado por Accessibility ID o Name
        result_display = wait.until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, "CalculatorResults")))

        print("Elementos de la calculadora localizados.")

        # 3. Ejecutar la operación: 7 + 3 =
        print("Ejecutando operación 7 + 3...")
        btn_seven.click()
        btn_plus.click()
        btn_three.click()
        btn_equal.click()

        # 4. Obtener y limpiar el resultado
        # El resultado se obtiene del atributo 'Name' o 'text' del elemento
        # Ejemplo de valor: "La pantalla es 10" (en español) o "Display is 10" (en inglés)
        raw_result = result_display.text.split()[-1]

        # Eliminamos comas o cualquier formato que no sea el número puro
        final_result = raw_result.replace(",", "")

        expected_result = "10"

        # 5. Aserto (Verificación)
        assert final_result == expected_result

        print(f"\n✅ PRUEBA EXITOSA: Resultado esperado: {expected_result}, Resultado obtenido: {final_result}")

    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBA: {e}")
        # Intentar obtener el título de la ventana para diagnóstico
        print(f"Título de la ventana actual: {driver.title}")

    finally:
        # 6. Cerrar la sesión y la aplicación
        if driver:
            driver.quit()
            print("\nConexión con WinAppDriver cerrada.")


if __name__ == '__main__':
    test_suma_calculadora()
    # log = True
    # run_behave("regression", False, "reports")
