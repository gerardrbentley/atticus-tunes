import os

DEBUG = True
# CRITICAL / ERROR / WARNING / INFO / DEBUG
LOG_LEVEL = 'DEBUG'

SERVER_NAME = os.getenv('SERVER_NAME')
SECRET_KEY = os.getenv('SECRET')

DATABASE_URI = f"{os.getenv('DATABASE_URL')}{os.getenv('DATABASE_NAME')}"
