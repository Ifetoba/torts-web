from .base import *
from environs import Env


# env= environs.Env()
env = Env()              # Get os environ
env.read_env(BASE_DIR / ".env")   # Read .env file

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','127.0.0.1', 'localhost']

