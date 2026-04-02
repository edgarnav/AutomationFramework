import configurations.configurations as configurations
import json
import os


class ManageCache:

    @staticmethod
    def get_cache_path(test_id):
        cache_dir = configurations.path_saved_testcases
        if not os.path.exists(cache_dir):
            try:
                os.makedirs(cache_dir, exist_ok=True)
            except OSError:
                pass
        return os.path.join(cache_dir, f"{test_id}.json")

    def load_test_step_cache(self, test_id):
        ruta = self.get_cache_path(test_id)
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_test_step_cache(self, test_id, data):
        ruta = self.get_cache_path(test_id)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
