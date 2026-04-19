from driver_interactions.element_interactions import ElementInteractions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from ai_actions.page_cleaner import PageCleaner
from ai_actions.ai_diagnosis import PerformDiagnosis
from ai_actions.ai_diagnosis import PerformDiagnosisAPI
from ai_actions.ai_diagnosis import PerformDiagnosisDB
from external_actions.saved_testcases_manager import ManageCache
from external_actions.perform_api_request import PerformAPIValidation
from external_actions.variable_manager import VariableManager
from pydantic import BaseModel, Field
import configurations as configurations
import external_actions.perform_db_query as db_actions
import utilities.prompts as prompt
import utilities.logger as log
import allure
from openai import OpenAI
import json
import os


class ResponseStructure(BaseModel):
    thinking: str = Field(description="Breve justificación de la acción")
    method: str = Field(description="Solo puede ser: 'click', 'write', 'read', 'verify', 'wait', 'scroll' o 'query_execution'")
    selector_type: str | None = Field(default=None, description="Debe ser: 'id', 'name', 'xpath' o 'data-testid', si aplica")
    selector_value: str | None = Field(default=None, description="El ID o atributo a interactuar, si aplica")
    text_value: str | None = Field(default=None, description="Texto a teclear, si aplica")
    variable_name: str | None = Field(default=None, description="Nombre de la variable en la cual se guardará el texto obtenido, si aplica")
    db_query: str | None = Field(default=None, description="Consulta a ejcutar en base de datos, si aplica")
    db_expected_result: str | None = Field(default=None, description="Resultado que se espera de ejecutar la consulta a base da datos, si aplica")
    db_result_variable: str | None = Field(default=None, description="Variable en la cual guardar el resultado obtenido de la consulta a base de datos, si aplica")
    db_url_key: str | None = Field(default=None, description="Llave de la variable de entorno de la cual obtener la URL, si aplica")


class AIActionDefinition(ElementInteractions, ManageCache, VariableManager):

    log = log.func_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.cleaner = PageCleaner
        self.diagnosis = PerformDiagnosis
        self.api_request = PerformAPIValidation
        self.diagnosis_api = PerformDiagnosisAPI
        self.diagnosis_db = PerformDiagnosisDB
        self.var_manager = VariableManager()

    def ai_action_definition(self, step, test_id, test_name):
        data_test = self.load_test_step_cache(test_id)
        step = self.var_manager.resolve_instruction(step)

        if not data_test:
            data_test = {"id": test_id, "name": test_name, "steps": {}}

        steps = data_test["steps"]

        if step.upper().startswith("API_REQUEST:"):
            config_json = json.loads(step.replace("API_REQUEST:", ""))
            success, response_server = self.api_request.perform_api_request(config_json)

            if not success:

                diagnosis_api = self.diagnosis_api.perform_diagnosis_api(response_server, config_json["expected_validate"])

                allure.attach(
                    json.dumps(diagnosis_api, indent=4, ensure_ascii=False),
                    name="🤖 AI DIAGNOSIS (API)",
                    attachment_type=allure.attachment_type.JSON
                )

                self.log.info(f"⚠️ Validation failed: {diagnosis_api['type_error']}")
                self.log.info(f"📝 Details: {diagnosis_api['detailed_analysis']}")

                return False

        with allure.step(f"Perform: {step}"):

            if step in steps:
                self.log.info(f"⚡ [FILE-CACHE] Using data from {test_id}.json")

                if steps[step].get("method") == "scroll":
                    locator_value = steps[step].get("selector_value")
                    locator_by_type = steps[step].get("selector_type")
                    max_swipes = 5

                    for attempt in range(max_swipes):
                        if self.scroll_to_element(locator_value, locator_by_type):
                            return True
                        elif attempt == max_swipes:
                            return False

                if self.perform_action_ai(steps[step]):
                    return True

            self.log.info(f"🤖 [IA] Learning new step for {test_id}...")
            action_ai = self.get_action_ai(step)

            if action_ai.get("method") == "scroll":
                locator_value = action_ai.get("selector_value")
                locator_by_type = action_ai.get("selector_type")
                max_swipes = 5
                for attempt in range(max_swipes):
                    if self.scroll_to_element(locator_value, locator_by_type):
                        data_test["steps"][step] = action_ai
                        self.save_test_step_cache(test_id, data_test)
                        self.log.info(f"💾 [SAVED] File {test_id}.json updated.")
                        return True
                    elif attempt <= max_swipes:
                        action_ai = self.get_action_ai(step)
                        locator_value = action_ai.get("selector_value")
                        locator_by_type = action_ai.get("selector_type")
                    else:
                        return False

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
                    json.dumps(diagnosis_api, indent=4, ensure_ascii=False),
                    name="CONCLUSION_IA_DIAGNOSIS",
                    attachment_type=allure.attachment_type.JSON
                )

                self.log.info(f"🚨 FINAL DIAGNOSIS: {diagnosis_api['type_error']} - {diagnosis_api['visual_analysis']}")
        return False

    def get_action_ai(self, action_test_case):

        source_page = self.get_source()
        page = self.cleaner_selector(source_page)

        try:
            prompt_system, prompt_user = prompt.prompt_get_action(action_test_case, page)
            client = OpenAI(base_url=os.environ.get("GENIUS_COPPEL_URL"))
            response = client.beta.chat.completions.parse(
                model='gemini/gemini-2.5-flash',
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user}
                ],
                response_format=ResponseStructure,
                temperature=0.1
            )
            action = response.choices[0].message.parsed.model_dump(exclude_none=True)

            return action

        except Exception as e:
            self.log.error(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            return False

    def perform_action_ai(self, action: dict) -> bool:

        method = action.get("method")
        locator_type = action.get("selector_type")
        locator_value = action.get("selector_value")
        text_value = action.get("text_value")

        if configurations.platform.lower() in ["android", "ios", "windows"]:
            if locator_type in ["id", "accessibility-id", "automation-id"]:
                locator_by_type = AppiumBy.ID
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

            elif method == "read":
                text = self.get_text(locator_value, locator_by_type)
                if text:
                    self.var_manager.set_variable(action.get("variable_name"), text)
                    return True
                else:
                    return False

            elif method == "query_execution":
                success, res_db = db_actions.perform_step_db(action, self.var_manager)
                if not success:
                    diagnosis_db = self.diagnosis_db.perform_diagnosis_db(res_db, action.get("db_expected_result"),
                                                                          action.get("db_query"))
                    allure.attach(json.dumps(diagnosis_db, indent=2, ensure_ascii=False), "Diagnosis AI DB")
                    self.log.error(res_db)
                    return False
                return success

            else:
                self.log.error(f"⚠️ Unknown method suggested by AI: {method}")
                return False

        except Exception as e:
            self.log.error(f"❌ Failed to interact with element. Error: {str(e)}")
            return False

    def cleaner_selector(self, source_page):

        if configurations.platform.lower() == "web":
            page = self.cleaner.clean_html(source_page)

        elif configurations.platform.lower() == "android":
            page = self.cleaner.clean_android_xml(source_page)

        elif configurations.platform.lower() == "ios":
            page = self.cleaner.clean_ios_xml(source_page)

        elif configurations.platform.lower() == "windows":
            page = self.cleaner.clean_desktop_html(source_page)

        else:
            self.log.error(f"❌ Platform is not valid: {configurations.platform}")
            assert False
        return page
