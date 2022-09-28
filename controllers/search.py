from flask import *
from ..models import db, get_enum, Inscriptions
from ..config import SETTINGS

search = Blueprint('search', __name__)

@search.route("/", methods=["GET"])
def index():
    return redirect(url_for('search.basic'))

@search.route("/basic", methods=["GET"])
def basic():
    return render_template("search/basic.html", get_enum=get_enum)

@search.route("/basic/do", methods=["GET"])
def basic_do():
    query = Inscriptions.query

    if 'mappola_id' in request.values.keys() and (mappola_id := request.values.get('mappola_id')) != '':
        query = query.filter_by(id=mappola_id)
    
    if 'province' in request.values.keys() and (province := request.values.get('province')) != '':
        query = query.filter_by(place_id=province)

    count = query.count()

    if count > 100:
        query = query.limit(100)

    results = query.all()

    return render_template("search/basic_do.html", results=results, count=count)