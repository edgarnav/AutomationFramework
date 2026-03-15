import json
import os
from datetime import datetime

# Carpeta raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_commands_for_test(case_id, tester_input):
    """
    Orquestador: Busca en el disco local antes de gastar tokens.
    """
    safe_id = case_id.replace(" ", "_").lower()
    file_path = os.path.join(ROOT_DIR, f"test_backup_{safe_id}.json")

    # 1. ¿Ya existe el respaldo?
    if os.path.exists(file_path):
        print(f"📦 [Cache] Cargando comandos locales para: {case_id}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['ai_commands']

    # 2. Si no existe, llamamos a la IA (Aquí iría tu lógica de Gemini)
    print(f"🤖 [IA] No hay respaldo. Consultando a Gemini para: {case_id}...")

    # --- SIMULACIÓN DE LLAMADA A GEMINI ---
    # Aquí es donde pondrías tu: response = model.generate_content(...)
    ai_response_commands = ["enter f4 with alt"]  # Ejemplo de lo que yo devolvería
    # --------------------------------------

    # 3. Guardamos para la próxima vez
    save_test_backup(case_id, tester_input, ai_response_commands)

    return ai_response_commands


def save_test_backup(case_id, tester_input, ai_commands):
    """Guarda el respaldo en la raíz."""
    safe_id = case_id.replace(" ", "_").lower()
    file_path = os.path.join(ROOT_DIR, f"test_backup_{safe_id}.json")

    data = {
        "test_case_id": case_id,
        "timestamp": datetime.now().isoformat(),
        "tester_steps": tester_input,
        "ai_commands": ai_commands
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"💾 [Sistema] Respaldo creado en la raíz para futuras ejecuciones.")

# --- MODO DE USO ---
# pasos_del_tester = "Cerrar la ventana con Alt F4"
# comandos_finales = get_commands_for_test("TC_001", pasos_del_tester)

# print(f"Ejecutando en testRigor: {comandos_finales}")