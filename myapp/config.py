from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Sets the base directory path
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected env variable '{}' not set.".format(name)
        raise Exception(message)

@dataclass
class ApplicationConfig(object):
    DB_TRACK_MODIFICATIONS = False
    DATABASE_URI: str = 'postgresql://postgres:admin@localhost:5432/collab-pre-1'

@dataclass
class JWtConfig(object):
    SECRET_KEY = get_env_variable(name='JWT_SECRET')

@dataclass
class EMAIL_NOTIFY(object):
    API  = f'''http://{get_env_variable(name='EMAIL_HOST')}:8083/api/'''