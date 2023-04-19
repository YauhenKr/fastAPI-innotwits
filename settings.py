import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class GlobalConfig(BaseSettings):
    AWS_REGION: str = os.getenv('AWS_REGION')
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY')
    ENVIRONMENT: str = "test"
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORYTHM: str = 'HS256'
    JWT_EXPIRATION_DELTA: str = 36000


config = GlobalConfig()
