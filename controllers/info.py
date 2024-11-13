from flask import *
from ..models import db, get_enum

info = Blueprint('info', __name__)

@info.route("/project/concept-and-aim")
def concept_and_aim(): return render_template("info/project/concept_and_aim.html")

@info.route("/project/team")
def team(): return render_template("info/project/team.html")

@info.route("/project/partners")
def partners(): return render_template("info/project/partners.html")

@info.route("/project/events-and-presentations")
def events_and_presentations(): return render_template("info/project/events_and_presentations.html")

@info.route("/project/acknowledgements")
def acknowledgements(): return render_template("info/project/acknowledgements.html")