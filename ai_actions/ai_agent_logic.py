from driver_interactions.element_interactions import ElementInteractions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from ai_actions.page_cleaner import PageCleaner
from ai_actions.ai_diagnosis import PerformDiagnosis
from ai_actions.ai_diagnosis import PerformDiagnosisAPI
from ai_actions.ai_diagnosis import PerformDiagnosisDB
from utilities.saved_testcases_manager import ManageCache
from utilities.perform_api_request import PerformAPIValidation
from utilities.variable_manager import VariableManager
from pydantic import BaseModel, Field
from google.genai import types
from google import genai
import configurations.configurations as configurations
import utilities.perform_db_query as db_actions
import configurations.prompts as prompt
import utilities.logger as log
import allure
import json


class ResponseStructure(BaseModel):
    thinking: str = Field(description="Breve justificación de la acción")
    method: str = Field(description="Solo puede ser: 'click', 'write', 'read', 'verify' o 'wait'")
    selector_type: str = Field(description="Debe ser: 'id', 'name', 'xpath' o 'data-testid'")
    selector_value: str = Field(description="El ID o atributo a interactuar")
    text_value: str | None = Field(default=None, description="Texto a teclear, si aplica")


class AIActionDefinition(ElementInteractions, ManageCache):

    log = log.func_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.cleaner = PageCleaner
        self.diagnosis = PerformDiagnosis
        self.api_request = PerformAPIValidation
        self.diagnosis_api = PerformDiagnosisAPI
        self.diagnosis_db = PerformDiagnosisDB
        self.var_manager = VariableManager

    def ai_action_definition(self, step, test_id, test_name):
        data_test = self.load_test_step_cache(test_id)

        if not data_test:
            data_test = {"id": test_id, "name": test_name, "steps": {}}

        steps = data_test["steps"]

        if step.startswith("DB_QUERY:"):
            config_db = json.loads(step.replace("DB_QUERY:", ""))
            success, res_db = db_actions.perform_step_db(config_db, self.var_manager)

            if not success:
                diagnosis_db = self.diagnosis_db.perform_diagnosis_db(res_db, config_db["expected"], config_db["query"])
                allure.attach(json.dumps(diagnosis_db, indent=2), "Diagnosis AI DB")
            return success

        elif step.startswith("API_REQUEST:"):
            config_json = json.loads(step.replace("API_REQUEST:", ""))
            success, response_server = self.api_request.perform_api_request(config_json)

            if not success:

                diagnosis_api = self.diagnosis_api.perform_diagnosis_api(response_server, config_json["expected_validate"])

                allure.attach(
                    json.dumps(diagnosis_api, indent=4),
                    name="🤖 AI DIAGNOSIS (API)",
                    attachment_type=allure.attachment_type.JSON
                )

                self.log.info(f"⚠️ Validation failed: {diagnosis_api['type_error']}")
                self.log.info(f"📝 Details: {diagnosis_api['detailed_analysis']}")

                return False

        with allure.step(f"Performing: {step}"):

            if step in steps:
                self.log.info(f"⚡ [FILE-CACHE] Using data from {test_id}.json")
                if self.perform_action_ai(steps[step]):
                    return True

            self.log.info(f"🤖 [IA] Learning new step for {test_id}...")
            action_ai = self.get_action_ai(step)

            if self.perform_action_ai(action_ai):
                data_test["steps"][step] = action_ai
                self.save_test_step_cache(test_id, data_test)
                self.log.info(f"💾 [SAVED] File {test_id}.json updated.")
                return True
            else:
                source_page = self.get_source()
                page = self.cleaner_selector(source_page)
                diagnosis_api = self.diagnosis.perform_auto_diagnosis(step, page, self.driver.get_screenshot_as_base64())
                allure.attach(self.driver.get_screenshot_as_png(), name="Failure_Capture",
                              attachment_type=allure.attachment_type.PNG)
                allure.attach(
                    json.dumps(diagnosis_api, indent=4),
                    name="CONCLUSION_IA_DIAGNOSIS",
                    attachment_type=allure.attachment_type.JSON
                )

                self.log.info(f"🚨 FINAL DIAGNOSIS: {diagnosis_api['type_error']} - {diagnosis_api['visual_analysis']}")
        return False

    def get_action_ai(self, action_test_case):

        source_page = self.get_source()
        page = self.cleaner_selector(source_page)

        try:
            client = genai.Client()
            response_ai = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt.prompt_get_action(action_test_case, page),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ResponseStructure,
                    temperature=0.1,
                ),
            )
            action = json.loads(response_ai.text)
            return action
        except Exception as e:
            self.log.error(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            return False

    def perform_action_ai(self, action: dict) -> bool:

        method = action.get("method")
        locator_type = action.get("selector_type")
        locator_value = action.get("selector_value")
        text_value = action.get("text_value")

        if configurations.platform in ['ios', 'windows']:
            if locator_type in ['id', 'accessibility-id', 'automation-id']:
                locator_by_type = AppiumBy.ACCESSIBILITY_ID
            elif locator_type == 'name':
                locator_by_type = AppiumBy.NAME
            else:
                locator_by_type = AppiumBy.XPATH
        else:
            locator_by_type = By.ID if locator_type == 'id' else By.XPATH

        try:
            self.log.info(f"🤖 Executing: {method.upper()} in {locator_type}='{locator_value}'...")
            if method == "click":
                return self.press_element(locator_value, locator_by_type)

            elif method == "write":
                return self.send_text(text_value, locator_value, locator_by_type)

            elif method == "verify":
                return self.is_element_displayed(locator_value, locator_by_type)

            else:
                self.log.error(f"⚠️ Unknown method suggested by AI: {method}")
                return False

        except Exception as e:
            self.log.error(f"❌ Failed to interact with element. Error: {str(e)}")
            return False

    def cleaner_selector(self, source_page):

        if configurations.platform == "web":
            page = self.cleaner.clean_html(source_page)

        elif configurations.platform == "android":
            page = self.cleaner.clean_android_xml(source_page)

        elif configurations.platform == "ios":
            page = self.cleaner.clean_ios_xml(source_page)

        elif configurations.platform == "windows":
            page = self.cleaner.clean_desktop_html(source_page)

        else:
            self.log.error(f"❌ Platform is not valid: {configurations.platform}")
            assert False
        return page
