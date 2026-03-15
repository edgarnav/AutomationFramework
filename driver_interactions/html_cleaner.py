from bs4 import BeautifulSoup


class HTMLCleaner:

    @staticmethod
    def clean_html(html_source):

        soup = BeautifulSoup(html_source, 'html.parser')
        interactive_elements = []

        tag_targets = ['button', 'input', 'a', 'select', 'textarea']

        for tag in soup.find_all(tag_targets):

            if tag.get('type') == 'hidden' or 'display: none' in str(tag.get('style', '')):
                continue

            data_element = {
                "tag": tag.name,
            }

            texto = tag.get_text(strip=True)
            if texto:
                data_element["texto"] = texto[:100]  # Máximo 100 caracteres

            useful_attributes = ['id', 'name', 'type', 'placeholder', 'aria-label', 'role']
            for attr in useful_attributes:
                if tag.has_attr(attr):
                    value = tag.get(attr)
                    if isinstance(value, list):
                        value = " ".join(value)
                    data_element[attr] = value

            if len(data_element) > 1:
                interactive_elements.append(data_element)

        return interactive_elements
