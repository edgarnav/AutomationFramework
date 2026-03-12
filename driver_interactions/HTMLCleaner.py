from bs4 import BeautifulSoup
import json


class HTMLCleaner:

    def limpiar_html_para_ia(html_source: str) -> list[dict]:
        """
        Analiza el HTML crudo y extrae solo los elementos interactivos
        relevantes para pruebas automatizadas.
        """
        soup = BeautifulSoup(html_source, 'html.parser')
        elementos_interactivos = []

        # Definimos las etiquetas que le importan a un Tester
        etiquetas_objetivo = ['button', 'input', 'a', 'select', 'textarea']

        # Buscamos todas las coincidencias en el DOM
        for etiqueta in soup.find_all(etiquetas_objetivo):

            # 1. Descartar elementos invisibles (muy comunes en frameworks modernos)
            if etiqueta.get('type') == 'hidden' or 'display: none' in str(etiqueta.get('style', '')):
                continue

            # 2. Inicializar el diccionario del elemento
            elemento_data = {
                "tag": etiqueta.name,
            }

            # 3. Extraer el texto visible (si tiene) y limitarlo para no saturar
            texto = etiqueta.get_text(strip=True)
            if texto:
                elemento_data["texto"] = texto[:100]  # Máximo 100 caracteres

            # 4. Extraer atributos clave para los selectores de Selenium
            atributos_utiles = ['id', 'name', 'type', 'placeholder', 'aria-label', 'role']
            for attr in atributos_utiles:
                if etiqueta.has_attr(attr):
                    valor = etiqueta.get(attr)
                    # Si es una lista (como las clases), lo unimos
                    if isinstance(valor, list):
                        valor = " ".join(valor)
                    elemento_data[attr] = valor

            # 5. Guardar el elemento solo si tiene atributos útiles o texto
            # (Descartamos botones vacíos sin ID ni texto)
            if len(elemento_data) > 1:
                elementos_interactivos.append(elemento_data)

        return elementos_interactivos
