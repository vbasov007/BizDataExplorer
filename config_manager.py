import yaml


class ViewConfigNotFound(Exception):
    pass


class YamlConfigManager:

    def __init__(self, yaml_path):
        with open(yaml_path) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def get_common_config(self):
        return self.config['common']

    def get_view_config(self, name: str):
        for v in self.config['views']:
            if v['name'] == name:
                return v
        raise ViewConfigNotFound(f'Config for "{name}" not found')
