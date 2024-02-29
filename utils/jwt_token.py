import jwt
import os
from flask import current_app

def generate_token(payload):
    encoded_jwt = jwt.encode(payload,current_app.config['SECRET_KEY'], algorithm="HS256")
    return encoded_jwt