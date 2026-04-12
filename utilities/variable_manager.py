import re


class VariableManager:

    def __init__(self):
        self.memory = {}

    def set_variable(self, key, value):
        self.memory[key] = str(value)

    def get_value(self, key):
        return self.memory.get(key, f"{{{{{{key}}}}}}")

    def resolve_instruction(self, step):
        def replace(match):
            key = match.group(1)
            return self.get_value(key)

        return re.sub(r"\{\{(.*?)}}", replace, step)
