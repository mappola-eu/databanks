from flask import *
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from .models import db, Role, User
from .config import SETTINGS
from .imports import import_
from .maintenance import maintenance

from . import controllers

import random

app = Flask(__name__, instance_path=SETTINGS['INSTANCE_PATH'])
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS['SQL_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mappola-databanks#secret_key'
app.config['SECURITY_PASSWORD_SALT'] = 'mappola-databanks#salt'
app.config['SECURITY_CHANGEABLE'] = True  # allow users to change their passwords
#app.config['SECURITY_REGISTERABLE'] = True  # allow users to change their passwords
app.config['MAPTILER_KEY'] = SETTINGS['MAPTILER_KEY']

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

@app.context_processor
def provide_global_template_data():
    return {
        "random_key": lambda: random.randint(1000, 9999)
    }

app.register_blueprint(controllers.inscriptions, url_prefix='/inscriptions')
app.register_blueprint(controllers.enum, url_prefix='/api/enum')
app.register_blueprint(controllers.resource, url_prefix='/r')
app.register_blueprint(controllers.search, url_prefix='/s')
app.register_blueprint(controllers.ext_zotero, url_prefix='/ext/zotero')
app.register_blueprint(import_)
app.register_blueprint(maintenance)