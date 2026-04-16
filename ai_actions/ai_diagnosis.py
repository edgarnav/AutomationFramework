from pydantic import BaseModel, Field
import configurations.prompts as prompt
import utilities.logger as logger
from openai import OpenAI
import os


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
            client = OpenAI(base_url=os.environ.get("GENIUS_COPPEL_URL"))
            response = client.beta.chat.completions.parse(
                model='gemini/gemini-2.5-flash',
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt.prompt_diagnosis(test_instruction, page)},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{screenshot_b64}"
                                }
                            }
                        ]
                    }
                ],
                response_format=AIDiagnosisModel,
                temperature=0.1
            )

            return response.choices[0].message.parsed.model_dump(exclude_none=True)

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
    def perform_diagnosis_api(endpoint, http_method, payload_sent, real_response, expected_result):
        log = logger.func_logger()

        try:
            prompt_system, prompt_user = prompt.prompt_diagnosis_api(endpoint, http_method, payload_sent, real_response, expected_result)
            client = OpenAI(base_url=os.environ.get("GENIUS_COPPEL_URL"))
            response = client.beta.chat.completions.parse(
                model='gemini/gemini-2.0-flash',
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user}
                ],
                response_format=AIDiagnosisAPIModel,
                temperature=0.1
            )
            return response.choices[0].message.parsed.model_dump(exclude_none=True)
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
            prompt_system, prompt_user = prompt.prompt_diagnosis_db(response_db, expected_criteria, query)
            client = OpenAI(base_url=os.environ.get("GENIUS_COPPEL_URL"))
            response = client.beta.chat.completions.parse(
                model='gemini/gemini-2.5-flash',
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user}
                ],
                response_format=AIDiagnosisDBModel,
                temperature=0.1
            )
            return response.choices[0].message.parsed.model_dump(exclude_none=True)
        except Exception as e:
            log.error(f'{{"error": "Something went wrong with LLM API: {str(e)}"}}')
            assert False
