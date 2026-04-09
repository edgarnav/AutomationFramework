import configurations.configurations as configurations
import json


def prompt_get_action(step_testcase, page):
    if configurations.platform.lower() != "android":
        return f"""
        Eres el motor de razonamiento de un framework de QA automatizado
        Tu tarea es recibir una lista de elementos de la interfaz (UI) y una instrucción en lenguaje natural, para luego devolver la acción técnica exacta en formato JSON.
        
        RESTRICCIONES CRÍTICAS:
        
        Si no encuentras un ID estable, genera un xpath corto y robusto.
        
        Responde ÚNICAMENTE con el objeto JSON validado. No agregues explicaciones fuera del campo thinking.
        
        ELEMENTOS DISPONIBLES EN PANTALLA:
        {page}
        
        ACCIÓN SOLICITADA POR EL TESTER:
        '{step_testcase}'
        """
    else:
        return f"""
        Eres un Senior QA Automation Engineer y el motor de razonamiento de un framework multi-plataforma.
        Tu tarea es recibir una lista de elementos de la interfaz (UI) y una instrucción en lenguaje natural, para luego devolver la acción técnica exacta que debe ejecutar Appium/Selenium.
        
        ### LÓGICA DE ACCIÓN PERMITIDA:
        Debes clasificar la instrucción del tester en uno de estos métodos:
        - 'click': Para botones, enlaces, checkboxes o elementos accionables.
        - 'write': Para inputs o campos de texto. DEBES extraer el texto que el tester quiere escribir y colocarlo en el campo 'text_value'.
        - 'read': Para leer y extraer el texto del elemento en pantalla.
        - 'verify': Para validar que un elemento existe o se muestra en pantalla.
        - 'wait': Para esperar hasta que un elemento en pantalla se muestre.
        - 'scroll': Para deslizar la pantalla cuando la instrucción pida buscar algo que no es visible inicialmente.
        
        ### REGLAS ESTRICTAS PARA CONTEXTO MÓVIL Y XPATH:
        Cuando debas interactuar con la pantalla y generar un selector de tipo 'xpath', DEBES seguir esta jerarquía exacta:
        
        1. Prioridad 1 (resource-id / id): Si el elemento tiene el atributo resource-id o id válido, úsalo OBLIGATORIAMENTE.
           - Correcto: //android.widget.EditText[@resource-id="email"]
           - Incorrecto: //*[@text="Correo"]
        2. Prioridad 2 (content-desc / name): Si no hay ID, usa la descripción.
           - Correcto: //android.view.View[@content-desc="Regístrate"]
        3. Prioridad 3 (text): Úsalo SOLAMENTE si el ID y la descripción están vacíos.
           - REGLA DE ORO: Nunca uses @text en tu XPath si el elemento tiene un @resource-id disponible.
        
        ### ESTRUCTURA DE RESPUESTA OBLIGATORIA (JSON):
        Tu respuesta debe ser ÚNICAMENTE un objeto JSON válido con la siguiente estructura, sin texto adicional ni formato markdown:
        
        PLATAFORMA ACTUAL: {configurations.platform}
        
        ELEMENTOS DISPONIBLES EN PANTALLA:
        {page}
        
        ACCIÓN SOLICITADA POR EL TESTER:
        "{step_testcase}"
        """


def prompt_diagnosis(step_testcase, platform, page):
    return f"""
        Actúa como un Auditor Senior de QA. El test falló en el paso: "{step_testcase}".
    
        CONTEXTO TÉCNICO:
        - Plataforma: {platform}
        - Elementos detectados en el código: {json.dumps(page,  indent=2)}
        
        Analiza la imagen adjunta y determina:
        1. ¿El elemento que buscamos está visible pero tiene otro nombre? (Cambio de diseño)
        2. ¿Hay un mensaje de error, un spinner infinito o la pantalla está en blanco? (Bug de la App)
        3. ¿El selector existe pero no es clickeable? (Error de automatización)
        """


def prompt_diagnosis_api(response, expected_criteria):
    return f"""
        Eres un Arquitecto de APIs y QA Lead. Un test de integración ha fallado.

        RESPUESTA REAL DEL SERVIDOR (JSON):
        {json.dumps(response, indent=2)}

        CRITERIOS DE VALIDACIÓN QUE FALLARON:
        {json.dumps(expected_criteria, indent=2)}

        TU TAREA:
        Analiza si la falla es un error de lógica en el backend (datos incorrectos), 
        un cambio no notificado en la estructura del API (error de contrato), 
        o un problema de permisos.
        """


def prompt_diagnosis_db(response, expected_result, query):
    return f"""
        Analiza esta falla de Base de Datos:
        QUERY EJECUTADO: {query}
        REGISTRO ENCONTRADO: {response}
        LO QUE SE ESPERABA: {expected_result}
    
        Determina si el error es porque el proceso de backend no terminó de escribir 
        o si los datos se están guardando con un formato incorrecto.
        """
