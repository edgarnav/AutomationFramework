from driver_interactions.element_interactions import ElementInteractions
from driver_interactions.init_driver import InitWebDriver
from driver_interactions.ai_agent_logic import GetResponseIA
import configurations.configurations as configurations
import pandas as pd
import pytest
import allure


def load_testcases_from_excel(path_file):
    df = pd.read_excel(path_file)

    test_cases = df.groupby(['id', 'name'])['step_description'].apply(list).reset_index()

    return test_cases.to_dict('records')


@allure.feature("AI-Modular-Caching")
@allure.severity(allure.severity_level.CRITICAL)
class TestSmartAutomation:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = InitWebDriver().init_driver()
        interactions_object = ElementInteractions(self.driver)
        interactions_object.launch_web_page(configurations.website)
        yield
        self.driver.quit()

    @pytest.mark.parametrize("case", load_testcases_from_excel("TestAIFramework.xlsx"))
    def test_smart_login_flow(self, case):
        test_id = case['id']
        test_name = case['name']
        steps = case['step_description']

        allure.dynamic.title(f"{test_id}: {test_name}")
        allure.dynamic.story(test_name)

        self.actions_ai_object = GetResponseIA(self.driver)
        for step in steps:
            result = self.actions_ai_object.testcase_saved_verification_definition(step, test_id, test_name)
            assert result is True, f"Fallo en {test_id} durante el paso: {step}"
