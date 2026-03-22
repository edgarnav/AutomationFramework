from driver_interactions.element_interactions import ElementInteractions
from pydantic import BaseModel, Field
import configurations.configurations as configurations
import configurations.prompts as prompt
import utilities.logger as log
from google.genai import types
from google import genai
import allure
import json
import base64


class AIDiagnosisModel(BaseModel):
    type_error: str = Field(description="Debe ser: 'BUG_APLICACION', 'CAMBIO_DISENO' o 'ERROR_AUTOMATIZACION'")
    visual_analysis: str = Field(description="Qué detectaste en la imagen vs la instrucción")
    is_blocker: bool
    technical_recommendation: str = Field(description="Cómo debería el programador o el tester arreglar esto")


class PerformDiagnosis:

    @staticmethod
    def perform_auto_diagnosis(test_instruction, page, screenshot_b64):
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt.prompt_diagnosis(test_instruction, configurations.platform, page),
                types.Part.from_bytes(data=base64.b64decode(screenshot_b64), mime_type="image/png")
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIDiagnosisModel
            )
        )
        return json.loads(response.text)
