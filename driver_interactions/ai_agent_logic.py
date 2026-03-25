from driver_interactions.element_interactions import ElementInteractions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from driver_interactions.page_cleaner import PageCleaner
from driver_interactions.ai_diagnosis import PerformDiagnosis
from utilities.manage_saved_testcases import ManageCache
from pydantic import BaseModel, Field
from google.genai import types
from google import genai
import configurations.configurations as configurations
import configurations.prompts as prompt
import utilities.logger as log
import allure
import json


class ResponseStructure(BaseModel):
    thinking: str = Field(description="Breve justificación de la acción")
    method: str = Field(description="Solo puede ser: click, escribir, leer, verificar o esperar")
    selector_type: str = Field(description="Debe ser: 'id', 'name', 'xpath' o 'data-testid'")
    selector_value: str = Field(description="El ID o atributo a interactuar")
    text_value: str | None = Field(default=None, description="Texto a teclear, si aplica")


class GetResponseIA(ElementInteractions, ManageCache):

    log = log.func_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.cleaner = PageCleaner
        self.diagnosis = PerformDiagnosis

    def testcase_saved_verification_definition(self, step, test_id, test_name):
        data_test = self.load_test_step_cache(test_id)

        if not data_test:
            data_test = {"id": test_id, "nombre": test_name, "pasos": {}}

        steps = data_test["pasos"]

        with allure.step(f"Ejecutando: {step}"):
            if step in steps:
                self.log.info(f"⚡ [FILE-CACHE] Usando datos de {test_id}.json")
                if self.perform_action_ai(steps[step]):
                    return True

            self.log.info(f"🤖 [IA] Aprendiendo nuevo paso para {test_id}...")
            action_ai = self.get_action_ai(step)

            if self.perform_action_ai(action_ai):
                data_test["pasos"][step] = action_ai
                self.save_test_step_cache(test_id, data_test)
                self.log.info(f"💾 [SAVED] Archivo {test_id}.json actualizado.")
                return True
            else:
                source_page = self.get_html()
                page = self.clean_page_source(source_page)
                diagnosis = self.diagnosis.perform_auto_diagnosis(step, page, self.driver.get_screenshot_as_base64())
                allure.attach(self.driver.get_screenshot_as_png(), name="Captura_Falla",
                              attachment_type=allure.attachment_type.PNG)
                allure.attach(
                    json.dumps(diagnosis, indent=4),
                    name="VEREDICTO_IA_DIAGNOSTICO",
                    attachment_type=allure.attachment_type.JSON
                )
                self.log.info(f"🚨 DIAGNÓSTICO FINAL: {diagnosis['type_error']} - {diagnosis['visual_analysis']}")
        return False

    def get_action_ai(self, action_test_case):

        source_page = self.get_html()
        page = self.clean_page_source(source_page)

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
            self.log.info(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            return False

    def perform_action_ai(self, action: dict) -> bool:

        method = action.get("method")
        locator_type = action.get("selector_type")
        locator_value = action.get("selector_value")
        text_value = action.get("text_value")

        if configurations.platform in ['android', 'ios', 'windows']:
            if locator_type in ['id', 'accessibility-id', 'automation-id']:
                locator_by_type = AppiumBy.ACCESSIBILITY_ID
            elif locator_type == 'nombre':
                locator_by_type = AppiumBy.NAME
            else:
                locator_by_type = AppiumBy.XPATH
        else:
            locator_by_type = By.ID if locator_type == 'id' else By.XPATH

        try:
            self.log.info(f"🤖 Ejecutando: {method.upper()} en {locator_type}='{locator_value}'...")
            if method == "click":
                return self.press_element(locator_value, locator_by_type)

            elif method == "escribir":
                return self.send_text(text_value, locator_value, locator_by_type)

            elif method == "verificar":
                return self.is_element_displayed(locator_value, locator_by_type)

            else:
                self.log.info(f"⚠️ Método desconocido sugerido por la IA: {method}")
                return False

        except Exception as e:
            self.log.info(f"❌ Fallo al interactuar con el elemento. Error: {str(e)}")
            return False

    def clean_page_source(self, source_page):

        if configurations.platform == "web":
            page = self.cleaner.clean_html(source_page)
        elif configurations.platform == "android":
            page = self.cleaner.clean_android_xml(source_page)
        elif configurations.platform == "ios":
            page = self.cleaner.clean_ios_xml(source_page)
        elif configurations.platform == "windows":
            page = self.cleaner.clean_desktop_html(source_page)
        else:
            self.log.error(f"❌La plataforma no es válida : {configurations.platform}")
            assert False
        return page
