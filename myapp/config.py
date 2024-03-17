from dataclasses import dataclass
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
env_var = dict(dotenv_values('.env'))

def get_env_variable(name):
    try:
        return env_var[name]
    except KeyError:
        message = "Expected env variable '{}' not set.".format(name)
        raise Exception(message)

@dataclass
class ApplicationConfig(object):
    DB_TRACK_MODIFICATIONS = False
    DATABASE_URI: str = 'postgresql://postgres:system@localhost:5432/collab-pre-1'

@dataclass
class JWtConfig(object):
    SECRET_KEY = get_env_variable(name='JWT_SECRET')

@dataclass
class EMAIL_NOTIFY(object):
    API  = f'''http://{get_env_variable(name='EMAIL_HOST')}:8083/api'''
