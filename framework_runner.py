from driver_interactions.element_interactions import ElementInteractions
from driver_interactions.init_webdriver import InitWebDriver
from driver_interactions.ai_agent_logic import GetResponseIA
import configurations.configurations as Configs
import pytest
import allure


@allure.feature("AI-Modular-Caching")
@allure.severity(allure.severity_level.CRITICAL)
class TestSmartAutomation:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = InitWebDriver().init_web_driver()
        interactions_object = ElementInteractions(self.driver)
        interactions_object.launch_web_page(Configs.website)
        yield
        self.driver.quit()

    def test_smart_login_flow(self):
        test_id, test_name = "TC-105", "Agregar producto a carrito"
        instructions = [
            "Escribe 'standard_user' en el campo de nombre de usuario",
            "Escribe 'secret_sauce' en el campo de contraseña",
            "Haz clic en el botón para iniciar sesión",
            "Haz clic en el primer producto que dice 'Sauce Labs Backpack",
            "Haz clic en el botón Add to cart para agregar el producto",
            "Verifica que el texto del botón haya cambiado a 'Remove'"
        ]
        self.actions_ai_object = GetResponseIA(self.driver)
        for step in instructions:
            with allure.step(f"Intent: {step}"):
                self.actions_ai_object.cache_verification_definition(step, test_id, test_name)
