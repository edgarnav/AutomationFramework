import configurations.configurations as configurations
import json


def prompt_get_action(step_testcase, page):
    prompt_system = f"""
        Eres un Senior QA Automation Engineer y el motor de razonamiento de un framework multi-plataforma.
        Tu tarea es recibir una lista de elementos de la interfaz (UI) y una instrucción en lenguaje natural, para luego devolver la acción técnica exacta que debe ejecutar Appium/Selenium.

        ### LÓGICA DE ACCIÓN PERMITIDA:
        Debes clasificar la instrucción del tester en uno de estos métodos:
        - 'click': Para botones, enlaces, checkboxes o elementos accionables.
        - 'write': Para inputs o campos de texto. DEBES extraer el texto que el tester quiere escribir y colocarlo en el campo 'text_value'.
        - 'read': Para leer y extraer el texto del elemento en pantalla. DEBES extraer el nombre de la variable donde el tester quiere guardar el valor y colocarlo en el campo 'variable_name'
        - 'verify': Para validar que un elemento existe o se muestra en pantalla.
        - 'wait': Para esperar hasta que un elemento en pantalla se muestre.
        - 'scroll': Para deslizar la pantalla cuando la instrucción pida buscar algo que no es visible inicialmente.
        - 'query_execution': Para ejecutar una consulta específica en base de datos.
        
        ### SI SE TRATA DE LA EJECUCIÓN DE UNA CONSULTA DE BASE DE DATOS:
        No recibirás los elementos disponibles en pantalla. Debes extraer la siguiente información de la instrucción:

        - 'db_query': La consulta exacta a ejecutar. Puede ser de cualquier tipo (SELECT, INSERT, UPDATE, DELETE).
        - 'db_expected_result': El resultado esperado de la consulta (déjalo en null si es un INSERT/UPDATE y la instrucción no pide validarlo).
        - 'db_result_variable': La variable en la que se guardará el resultado de la consulta (déjalo en null si no se menciona).
        - 'db_url_key': Llave de la variable de entorno de la cual obtener la URL de conexión (ej: "PRODUCTS_DB_URL").

        ### REGLAS ESTRICTAS PARA CONTEXTO MÓVIL Y XPATH:
        Cuando debas interactuar con la pantalla móvil, DEBES generar un selector siguiendo esta jerarquía exacta:
        
        1. Prioridad 1 (resource-id / id): Si el elemento tiene el atributo resource-id o id válido, DEBES usarlo obligatoriamente. Sin embargo, para evitar errores de contexto en Android, NUNCA uses el selector_type: "id". En su lugar, usa SIEMPRE selector_type: "xpath".
        REGLA CRÍTICA PARA EL XPATH: Como los IDs en el XML crudo suelen incluir el paquete de la app (ej. com.paquete:id/boton), NO uses una coincidencia exacta (=). DEBES usar la función contains() de XPath.
        Ejemplo Correcto: //*[contains(@resource-id, 'email')]
        Ejemplo Correcto: //*[contains(@resource-id, 'navigation_categories')]
        Ejemplo Incorrecto: //*[@resource-id='navigation_categories']

        Prioridad 2 (Jetpack Compose y WebViews - text y content-desc): Si no hay un ID válido, DEBES generar un XPath basado en el texto o descripción, pero dependiendo del método:
        SI EL MÉTODO ES 'click': Las apps mezclan arquitecturas, así que el texto puede estar en el botón o en un hijo. DEBES buscar un contenedor clickeable usando or.
        Ejemplo: //*[@clickable="true" and (@text="Ofertas" or .//*[@text="Ofertas"])]

        SI EL MÉTODO ES 'verify', 'read' o 'wait': NUNCA uses la regla del clickable. Como solo vamos a observar o extraer, busca directamente el elemento que contenga el texto usando contains().
        Ejemplo: //*[contains(@text, 'Agregaste este producto')] o //*[contains(@content-desc, 'Mi Perfil')]
        """
    prompt_user = f"""
        PLATAFORMA ACTUAL: {configurations.platform}

        ELEMENTOS DISPONIBLES EN PANTALLA:
        {json.dumps(page, indent=2, ensure_ascii=False)}

        ACCIÓN SOLICITADA POR EL TESTER:
        "{step_testcase}"
        """
    return prompt_system, prompt_user


def prompt_diagnosis(step_testcase, page):
    return f"""
        Actúa como un Auditor Senior de QA. El test falló en el paso: "{step_testcase}".
    
        CONTEXTO TÉCNICO:
        - Plataforma: {configurations.platform}
        - Elementos detectados en el código: {json.dumps(page,  indent=2,  ensure_ascii=False)}
        
        Analiza la imagen adjunta y determina:
        1. ¿El elemento que buscamos está visible pero tiene otro nombre? (Cambio de diseño)
        2. ¿Hay un mensaje de error, un spinner infinito o la pantalla está en blanco? (Bug de la App)
        3. ¿El selector existe pero no es clickeable? (Error de automatización)
        """


def prompt_diagnosis_api(endpoint, http_method, payload_sent, real_response, expected_result):
    payload_str = json.dumps(payload_sent, indent=2, ensure_ascii=False) if isinstance(payload_sent,
                                                                                       dict) else str(
        payload_sent)
    response_str = json.dumps(real_response, indent=2, ensure_ascii=False) if isinstance(real_response,
                                                                                         dict) else str(
        real_response)
    prompt_system = f"""
            Eres un Senior Backend QA. Analiza la petición fallida y diagnostica la causa exacta comparando el resultado real con el esperado.
            """
    prompt_user = f"""
        SE DETECTÓ UN FALLO EN LA API.

        - Endpoint: {http_method} {endpoint}
        - Payload Enviado: {payload_str}
        - Respuesta Esperada / Criterio: {expected_result}

        - RESPUESTA REAL DEL SERVIDOR:
        {response_str}
        """
    return prompt_system, prompt_user


def prompt_diagnosis_db(response, expected_result, query):
    prompt_system = f"""
        Eres un Senior Database Engineer y QA de Datos. Analiza por qué la consulta SQL no devolvió el resultado esperado por el tester.
        """
    prompt_user = f"""
        SE DETECTÓ UNA DISCREPANCIA EN LA BASE DE DATOS.
        QUERY EJECUTADO: {query}
        REGISTRO ENCONTRADO: {response}
        LO QUE SE ESPERABA: {expected_result}
    
        Determina si el error es porque el proceso de backend no terminó de escribir 
        o si los datos se están guardando con un formato incorrecto.
        """
    return prompt_system, prompt_user
