from flask import *
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from .models import db, Role, User
from .config import SETTINGS

from . import controllers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS['SQL_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mappola-databanks#secret_key'
app.config['SECURITY_PASSWORD_SALT'] = 'mappola-databanks#salt'

db.init_app(app)
migrate = Migrate(app, db)
app.db = db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route("/")
def index():
    return render_template("index.html")

@app.template_filter()
def camel2human(name):
    naming_parts = [""]
    for c in name:
        if c.upper() == c:
            naming_parts += [c]
        else:
            naming_parts[-1] += c
    return " ".join(naming_parts)

app.register_blueprint(controllers.inscriptions, url_prefix='/inscriptions')
app.register_blueprint(controllers.enum, url_prefix='/api/enum')
app.register_blueprint(controllers.resource, url_prefix='/r')