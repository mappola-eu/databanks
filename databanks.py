from flask import *
from flask_migrate import Migrate
from .models import db
from .config import SETTINGS

from . import controllers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS['SQL_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.db = db

@app.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(controllers.inscriptions, url_prefix='/inscriptions')