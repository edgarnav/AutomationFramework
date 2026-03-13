from driver_interactions.ElementInteractions import ElementInteractions
from driver_interactions.InitWebDriver import InitWebDriver
from driver_interactions.AIAgentLogic import GetResponseIA
import configurations.ConfigFile as Configs
import pytest
import allure


@pytest.fixture(scope="class")
def driver_setup(request):
    driver = InitWebDriver().init_web_driver()
    interactions_object = ElementInteractions(driver)
    interactions_object.launch_web_page(Configs.website)
    request.cls.driver = driver

    yield  # Tests run here

    driver.quit()


@allure.feature("AI-Driven Automation")
@pytest.mark.usefixtures("driver_setup")  # This applies the setup to the whole class
class TestAIAgent:

    @allure.story("Dynamic User Login Flow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_smart_login_flow(self):
        # Notice we now use self.driver instead of just driver
        self.actions_ai_object = GetResponseIA(self.driver)

        instrucciones = [
            "Escribe 'standard_user' en el campo de nombre de usuario",
            "Escribe 'secret_sauce' en el campo de contraseña",
            "Haz clic en el botón para iniciar sesión",
            "Haz clic en el primer producto que dice 'Sauce Labs Backpack",
            "Haz clic en el botón Add to cart para agregar el producto",
            "Verifica que el texto del botón haya cambiado a 'Remove'"
        ]
        for paso in instrucciones:
            with allure.step(f"Intent: {paso}"):
                self.actions_ai_object.get_action_ai(paso)
