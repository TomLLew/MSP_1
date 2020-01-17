from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from application import routes