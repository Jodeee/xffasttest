import os
import yaml
from xffasttest.common import Dict

class Utils:

    @staticmethod
    def traverse_dir(directory: str) -> list:
        test_files: list = []
        for root, dirs, files in os.walk(directory):
            for file in files:

                if not file.endswith('.py') or file == '__init__.py':
                    continue 

                file_path = os.path.join(root, file)

                if os.path.isfile(file_path): 
                    test_files.append(file_path)
        return test_files

    @staticmethod
    def load_yaml(path) -> Dict:
        with open(path, "r", encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            yaml_dict = Dict()
            if yaml_data:
                for key, value in yaml_data.items():
                    yaml_dict[key] = value
        return yaml_dict