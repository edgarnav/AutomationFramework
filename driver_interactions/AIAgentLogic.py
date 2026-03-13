from driver_interactions.ElementInteractions import ElementInteractions
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from selenium.webdriver.common.by import By
import json
from driver_interactions.HTMLCleaner import HTMLCleaner
import utilities.Logger as Log


class ResponseStructure(BaseModel):
    thinking: str = Field(description="Breve justificación de la acción")
    method: str = Field(description="Solo puede ser: click, escribir, leer, verificar o esperar")
    selector_type: str = Field(description="Debe ser: 'id', 'name', 'xpath' o 'data-testid'")
    selector_value: str = Field(description="El ID o atributo a interactuar")
    text_value: str | None = Field(default=None, description="Texto a teclear, si aplica")


class GetResponseIA(ElementInteractions):

    log = Log.func_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.cleaner = HTMLCleaner

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
            self.perform_action_ai(action)
        except Exception as e:
            self.log.info(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            assert False

    def perform_action_ai(self, response_ai: dict) -> bool:
        method = response_ai.get("method")
        locator_type = response_ai.get("selector_type")
        locator_value = response_ai.get("selector_value")
        text_value = response_ai.get("text_value")

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
