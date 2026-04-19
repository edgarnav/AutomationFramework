from driver_interactions.element_interactions import ElementInteractions
from driver_interactions.init_driver import InitWebDriver
from ai_actions.ai_agent_logic import AIActionDefinition
import configurations as configurations
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
    def setup(self, case):
        self.driver = InitWebDriver().init_driver(case['id'], case['name'])
        ElementInteractions(self.driver)
        yield
        self.driver.quit()

    @pytest.mark.parametrize("case", load_testcases_from_excel(configurations.matrix_testcases_path))
    def test_smart_login_flow(self, case):
        testcase_id = case['id']
        testcase_name = case['name']
        steps = case['step_description']

        allure.dynamic.title(f"{testcase_id}: {testcase_name}")

        self.actions_ai_object = AIActionDefinition(self.driver)
        for step in steps:
            result = self.actions_ai_object.ai_action_definition(step, testcase_id, testcase_name)
            assert result is True, f"Fallo en {testcase_id} durante el paso: {step}"
