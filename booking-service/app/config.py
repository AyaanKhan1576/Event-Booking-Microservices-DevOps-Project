import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:minahil.ali117@localhost:5432/bookingdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'pyamqp://guest@localhost//')  # RabbitMQ URL
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # You should generate a proper secret key
