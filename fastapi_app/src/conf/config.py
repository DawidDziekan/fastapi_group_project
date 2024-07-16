from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    sqlalchemy_database_url: str = os.getenv('DATABASE_URL')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = "HS256"
    mail_username: str = os.getenv('MAIL_USERNAME')
    mail_password: str = os.getenv('MAIL_PASSWORD')
    mail_from: str = os.getenv('MAIL_FROM')
    mail_port: str = os.getenv('MAIL_PORT')
    mail_server: str = os.getenv('MAIL_SERVER')
    redis_host: str = os.getenv('REDIS_HOST')
    redis_port: str = os.getenv('REDIS_PORT')
    redis_password: str = os.getenv('REDIS_PASSWORD', None)
    cloudinary_name: str = os.getenv('CLOUDINARY_CLOUD_NAME')
    cloudinary_api_key: str = os.getenv('CLOUDINARY_API_KEY')
    cloudinary_api_secret: str = os.getenv('CLOUDINARY_API_SECRET')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
