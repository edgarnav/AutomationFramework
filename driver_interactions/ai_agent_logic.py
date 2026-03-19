from driver_interactions.element_interactions import ElementInteractions
from selenium.webdriver.common.by import By
from driver_interactions.html_cleaner import HTMLCleaner
from utilities.manage_saved_testcases import ManageCache
from pydantic import BaseModel, Field
from google.genai import types
from google import genai
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
        self.cleaner = HTMLCleaner

    def cache_verification_definition(self, step, test_id, test_name):
        data_test = self.load_test_step_cache(test_id)

        # Si el archivo no existe, creamos la estructura base
        if not data_test:
            data_test = {"id": test_id, "nombre": test_name, "pasos": {}}

        steps = data_test["pasos"]

        with allure.step(f"Ejecutando: {step}"):
            # Escenario A: Buscar en su archivo JSON propio
            if step in steps:
                self.log.info(f"⚡ [FILE-CACHE] Usando datos de {test_id}.json")
                if self.perform_action_ai(steps[step]):
                    return True

            # Escenario B: Si no está en su archivo, consultar IA
            self.log.info(f"🤖 [IA] Aprendiendo nuevo paso para {test_id}...")
            action_ai = self.get_action_ai(step)

            if self.perform_action_ai(action_ai):
                # Guardar solo en el archivo de este test
                data_test["pasos"][step] = action_ai
                self.save_test_step_cache(test_id, data_test)
                self.log.info(f"💾 [SAVED] Archivo {test_id}.json actualizado.")
                return True
        return False

    def get_action_ai(self, action_test_case):
        html_page = self.get_html()
        page = self.cleaner.clean_html(html_page)
        client = genai.Client()
        prompt = f"""
                Eres el motor de razonamiento de un framework de QA automatizado.

                ELEMENTOS DISPONIBLES EN PANTALLA:
                {page}

                ACCIÓN SOLICITADA POR EL TESTER:
                '{action_test_case}'
                """
        try:
            response_ai = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
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
            assert False

    def perform_action_ai(self, action: dict) -> bool:
        method = action.get("method")
        locator_type = action.get("selector_type")
        locator_value = action.get("selector_value")
        text_value = action.get("text_value")

        selector_by = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
        }

        if locator_type == "data-testid":
            locator_by_type = By.XPATH
            locator_value = f"//*[@data-testid='{locator_value}']"
        else:
            locator_by_type = selector_by.get(locator_type, By.ID)

        try:
            self.log.info(f"🤖 Ejecutando: {method.upper()} en {locator_type}='{locator_value}'...")
            if method == "click":
                self.press_element(locator_value, locator_by_type)

            elif method == "escribir":
                self.send_text(text_value, locator_value, locator_by_type)

            elif method == "verificar":
                self.is_element_displayed(locator_value, locator_by_type)

            else:
                self.log.info(f"⚠️ Método desconocido sugerido por la IA: {method}")
                return False

            return True

        except Exception as e:
            self.log.info(f"❌ Fallo al interactuar con el elemento. Error: {str(e)}")
            return False
