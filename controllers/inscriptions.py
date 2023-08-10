from flask import Blueprint, url_for, render_template
from ..models import Inscriptions, db, get_enum, inscriptions_to_json
from ..models import ObjectDecorationTags, Languages, VerseTypes, DatingCriteria
from flask_security import login_required

inscriptions = Blueprint('inscriptions', __name__)


@inscriptions.route("/map")
def map():
    inscs = Inscriptions.query.all()

    mc = inscriptions_to_json(inscs)

    return render_template("inscriptions/map.html", mc=mc)
