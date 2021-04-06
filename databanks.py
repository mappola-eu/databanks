from flask import *
from flask_migrate import Migrate
from .models import db
from .config import SETTINGS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS['SQL_URL']

db.init_app(app)
migrate = Migrate(app, db)
app.db = db

@app.route("/")
def index():
    return render_template("index.html")