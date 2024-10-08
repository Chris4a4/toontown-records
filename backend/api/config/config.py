import yaml
import os

class Config:
    WEBHOOK_URL = ''
    OAUTH_URL = ''
    OAUTH_CLIENT = ''
    OAUTH_SECRET = ''

    MAX_NAME_LEN = 0
    MIN_NAME_LEN = 0

    @classmethod
    def public_config(cls, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)

            cls.MAX_NAME_LEN = data['MAX_NAME_LEN']
            cls.MIN_NAME_LEN = data['MIN_NAME_LEN']
    
    @classmethod
    def private_config(cls, filepath):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            
            cls.WEBHOOK_URL = data['WEBHOOK_URL']
            cls.OAUTH_URL = data['OAUTH_URL']
            cls.OAUTH_CLIENT = data['OAUTH_CLIENT']
            cls.OAUTH_SECRET = data['OAUTH_SECRET']


public_path = os.path.join(os.path.dirname(__file__), '..', '..', 'public_config.yaml')
Config.public_config(public_path)

private_path = os.path.join(os.path.dirname(__file__), '..', '..', 'private_config.yaml')
Config.private_config(private_path)