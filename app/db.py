from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from .models.base import Base

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
