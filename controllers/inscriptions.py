from flask import Blueprint, url_for, render_template, make_response, abort
from ..models import Inscriptions, db, get_enum, inscriptions_to_json
from ..models import ObjectDecorationTags, Languages, VerseTypes, DatingCriteria
from flask_security import login_required

inscriptions = Blueprint('inscriptions', __name__)


@inscriptions.route("/map")
def map():
    inscs = Inscriptions.query.all()

    mc = inscriptions_to_json(inscs)

    return render_template("inscriptions/map.html", mc=mc)


@inscriptions.route("/MPL<id>.xml")
def render_xml(id):
    insc = Inscriptions.query.filter_by(id=int(id)).one_or_none()

    if not insc:
        abort(404)

    xml_file = render_template("inscriptions/one.xml", insc=insc)
    response = make_response(xml_file)
    response.headers['Content-Type'] = 'application/xml'

    return response

