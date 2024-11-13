from flask import *
from ..models import db, get_enum

info = Blueprint('info', __name__)

@info.route("/project/concept-and-aim")
def concept_and_aim():
    return render_template("info/project/concept_and_aim.html")