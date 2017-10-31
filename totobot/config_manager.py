import os
import json


class ConfigurationManager:

    def __init__(self, base_dir='~/.totobot', c_name='config.json'):

        base_dir = os.path.expanduser(base_dir)
        config_file = os.path.join(base_dir, c_name)

        with open(config_file, 'r') as f:
            config_json = json.load(f)

        self.MICROSOFT_APP_ID = config_json['MICROSOFT_APP_ID']
        self.MICROSOFT_APP_PASSWORD = config_json['MICROSOFT_APP_PASSWORD']
        self.LUIS_APP_CHAIN = config_json['LUIS_APP_CHAIN']
        self.LUIS_SUB_KEY = config_json['LUIS_SUB_KEY']
        self.TOTOBOT_KEY = config_json['TOTOBOT_KEY']
