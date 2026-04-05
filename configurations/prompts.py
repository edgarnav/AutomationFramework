import configurations.configurations as configurations
import json


def prompt_get_action(step_testcase, page):
    if configurations.platform != "android":
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
        Eres el motor de razonamiento de un framework de QA automatizado
        Tu tarea es recibir una lista de elementos de la interfaz (UI) y una instrucción en lenguaje natural, para luego devolver la acción técnica exacta en formato JSON.
        
        RESTRICCIONES CRÍTICAS:
        
        Si no encuentras un ID estable y la acción no requiere hacer un clic, genera un xpath robusto.
        
        REGLA DE XPATH PARA MÓVILES ÚNICAMENTE SI LA ACCIÓN ES REALIZAR UN CLIC (JETPACK COMPOSE/REACT NATIVE):
        Si necesitas hacer clic a un elemento basado en su texto o descripción, NUNCA generes un XPath que apunte directamente al TextView si este no es explícitamente clickeable. Debes generar un XPath que apunte a su contenedor clickeable usando esta estructura:
        //*[@clickable='true' and .//*[@text='EL_TEXTO_AQUI']] o //*[@clickable='true' and .//*[@content-desc='EL_TEXTO_AQUI']].
        
        Responde ÚNICAMENTE con el objeto JSON validado. No agregues explicaciones fuera del campo thinking.
        
        ELEMENTOS DISPONIBLES EN PANTALLA:
        {page}
        
        ACCIÓN SOLICITADA POR EL TESTER:
        '{step_testcase}'
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
