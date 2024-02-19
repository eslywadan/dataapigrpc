import json
import os

class SecretLoader:
    _secret_all = {}

    @classmethod
    def secret(cls, catalog):
        if len(cls._secret_all) == 0:
            filename = os.path.join('ext/config', 'secret.json')
            with open(filename) as json_file:
                cls._secret_all = json.load(json_file)
        
        return cls._secret_all[catalog]


    @classmethod
    def reset_secret_loader(cls):
        cls._secret_all = {}
