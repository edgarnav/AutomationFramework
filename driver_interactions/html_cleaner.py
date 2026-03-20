from bs4 import BeautifulSoup
from lxml import etree


class HTMLCleaner:

    @staticmethod
    def clean_html(html_source):

        soup = BeautifulSoup(html_source, 'html.parser')
        cleaned_elements = []

        tag_targets = ['button', 'input', 'a', 'select', 'textarea']

        for tag in soup.find_all(tag_targets):

            if tag.get('type') == 'hidden' or 'display: none' in str(tag.get('style', '')):
                continue

            data_element = {
                "tag": tag.name,
            }

            texto = tag.get_text(strip=True)
            if texto:
                data_element["texto"] = texto[:100]

            useful_attributes = ['id', 'name', 'type', 'placeholder', 'aria-label', 'role']
            for attr in useful_attributes:
                if tag.has_attr(attr):
                    value = tag.get(attr)
                    if isinstance(value, list):
                        value = " ".join(value)
                    data_element[attr] = value

            if len(data_element) > 1:
                cleaned_elements.append(data_element)

        return cleaned_elements

    @staticmethod
    def clean_android_xml(xml_source):

        root = etree.fromstring(xml_source.encode('utf-8'))
        cleaned_elements = []

        for elem in root.xpath("//*[@clickable='true' or @focusable='true']"):
            item = {
                "class": elem.get("class").split('.')[-1],
                "text": elem.get("text", "")[:50],
                "resource-id": elem.get("resource-id", "").split('/')[-1],
                "content-desc": elem.get("content-desc", ""),
                "enabled": elem.get("enabled")
            }
            if item["text"] or item["resource-id"] or item["content-desc"]:
                cleaned_elements.append(item)
        return cleaned_elements

    @staticmethod
    def clean_ios_xml(xml_source):

        root = etree.fromstring(xml_source.encode('utf-8'))
        cleaned_elements = []

        elements = [
            'Button', 'TextField', 'SecureTextField', 'Link',
            'StaticText', 'Cell', 'Switch', 'SearchField'
        ]

        xpath_query = " | ".join([f"//XCUIElementType{t}[@visible='true']" for t in elements])

        for elem in root.xpath(xpath_query):

            item = {
                "type": elem.tag.replace('XCUIElementType', ''),
                "name": elem.get("name", ""),
                "label": elem.get("label", ""),
                "value": elem.get("value", ""),
                "enabled": elem.get("enabled", "true")
            }

            if item["name"] or item["label"] or item["value"]:
                cleaned_elements.append(item)

        return cleaned_elements

    @staticmethod
    def clean_desktop_html(xml_source):

        root = etree.fromstring(xml_source.encode('utf-8'))
        cleaned_elements = []

        for elem in root.xpath("//*[@IsOffscreen='False']"):
            item = {
                "type": elem.get("ControlType", "").replace("ControlType.", ""),
                "automation-id": elem.get("AutomationId", ""),
                "name": elem.get("Name", ""),
                "class": elem.get("ClassName", ""),
                "enabled": elem.get("IsEnabled", "True")
            }

            if item["automation-id"] or item["name"]:
                cleaned_elements.append(item)

        return cleaned_elements
