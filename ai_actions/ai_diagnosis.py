from pydantic import BaseModel, Field
import configurations.configurations as configurations
import configurations.prompts as prompt
from google.genai import types
from google import genai
import utilities.logger as logger
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
        log = logger.func_logger()
        try:
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
        except Exception as e:
            log.error(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            assert False


class AIDiagnosisAPIModel(BaseModel):
    type_error: str = Field(description="Debe ser: 'ERROR_DATOS', 'ERROR_CONTRATO', 'ERROR_SERVIDOR' o 'ERROR_AUTENTICACION'")
    detailed_analysis: str = Field(description="Explicación técnica de la discrepancia encontrada")
    severity: str = Field(description="Alta, Media o Baja")
    json_path_affected: str = Field(description="La ruta del campo que falló (ej: data.user.id)")
    technical_recommendation: str = Field(description="Instrucción para el desarrollador para corregir el bug")


class PerformDiagnosisAPI:

    @staticmethod
    def perform_diagnosis_api(response_api, expected_criteria):
        log = logger.func_logger()

        try:
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt.prompt_diagnosis_api(response_api, expected_criteria),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AIDiagnosisAPIModel,
                    temperature=0.1
                )
            )

            return json.loads(response.text)
        except Exception as e:
            log.error(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            assert False


class AIDiagnosisDBModel(BaseModel):
    type_error: str = Field(description="¿Es un bug de persistencia, datos truncados o registro no encontrado?")
    query_analysis: str = Field(description="Evaluación de si el query ejecutado era el correcto")
    severity: str = Field(description="Crítica si no hay registro, Media si es un campo incorrecto")


class PerformDiagnosisDB:

    @staticmethod
    def perform_diagnosis_db(response_db, expected_criteria, query):
        log = logger.func_logger()

        try:
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt.prompt_diagnosis_db(response_db, expected_criteria, query),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AIDiagnosisAPIModel,
                    temperature=0.1
                )
            )
            return json.loads(response.text)
        except Exception as e:
            log.error(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            assert False
