from flask import *
from ..models import db, get_enum
from flask_security import login_required

enum = Blueprint('enum', __name__)

@enum.route("/<name>")
def show(name):
    try:
        enum = get_enum(name)
    except: abort(403)

    return render_template("enum/show.html", name=name, enum=enum)