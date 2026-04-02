import requests
import utilities.logger as log


class PerformAPIValidation:

    @staticmethod
    def perform_api_request(config_json):

        url = config_json.get("url")
        method = config_json.get("method", "GET").upper()
        headers = config_json.get("headers", {})
        body = config_json.get("body", {})
        validations = config_json.get("expected_validate", {})

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=body if method != "GET" else None,
                timeout=15
            )

            res_json = response.json() if response.text else {}

            errors = []

            if "status_code" in validations:
                if response.status_code != validations["status_code"]:
                    errors.append(f"Status Code expected {validations['status_code']}, but was {response.status_code}")

            for key, expected_value in validations.items():
                if key == "status_code": continue

                # Aquí podrías usar una librería como 'jsonpath-ng' para búsquedas complejas,
                # pero por ahora validamos si la llave existe en el primer nivel.
                valor_real = res_json.get(key)
                if valor_real != expected_value:
                    errors.append(f"Field '{key}' expected '{expected_value}', but was '{valor_real}'")

            if errors:
                return False, f"Failed validation in API: {', '.join(errors)}"

            return True, res_json

        except Exception as e:
            return False, f"Error request API: {str(e)}"
