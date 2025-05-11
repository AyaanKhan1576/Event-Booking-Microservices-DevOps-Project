from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from dotenv import load_dotenv
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Load configurations
app.config.from_object('app.config.Config')

# Initialize the database and migrate instances
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Import routes, models, and tasks after initializing the app
from app import views, models, tasks

from prometheus_flask_exporter import PrometheusMetrics

# Attach Prometheus metrics to the Flask app
metrics = PrometheusMetrics(app)
