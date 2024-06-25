from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# Print environment variables to debug
print("DATABASE_URL from .env:", os.environ.get('DATABASE_URL'))
print("Loaded DATABASE_URL:", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
