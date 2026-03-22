import json


def prompt_get_action(step_testcase, page):
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
