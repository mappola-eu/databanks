from flask import *
from ..models import db, get_enum, Inscriptions, Places, ModernRegions
from ..config import SETTINGS

from sqlalchemy import select

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
    places = Places.query

    if 'mappola_id' in request.values.keys() and (mappola_id := request.values.get('mappola_id')) != '':
        query = query.filter(Inscriptions.id==mappola_id)
    
    if 'province' in request.values.keys() and (province := request.values.get('province')) != '':
        places = places.filter(Places.province_id==province)

    if 'region' in request.values.keys() and (region := request.values.get('region')) != '':
        places = places.filter(Places.modern_region_id==region)

    if 'state' in request.values.keys() and (state := request.values.get('state')) != '':
        regions_in_state = [i.id for i in ModernRegions.query.filter_by(state_id=state).all()]
        places = places.filter(Places.id.in_(regions_in_state))

    if 'date_min' in request.values.keys() and (date_min := request.values.get('date_min')) != '':
        query = query.filter(Inscriptions.date_begin >= date_min)

    if 'date_max' in request.values.keys() and (date_max := request.values.get('date_max')) != '':
        query = query.filter(Inscriptions.date_end <= date_max)


    query = query.filter(Inscriptions.place_id.in_([i[0] for i in places.values(Places.id)]))

    if 'text1' in request.values.keys() and (text1 := request.values.get('text1')) != '':
        text_1_query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text1}%"))
    else:
        text_1_query = None
    
    if 'text2' in request.values.keys() and (text2 := request.values.get('text2')) != '':
        text_2_query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text2}%"))
    else:
        text_2_query = None

    if 'text1' in request.values.keys() and (text1 := request.values.get('text1')) != '' and \
        'text2' in request.values.keys() and (text2 := request.values.get('text2')) != '':
        
        if request.values.get('text_conj', 'AND') == 'OR':
            query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text1}%")) \
                .union(query.filter(Inscriptions.text_epidoc_form.like(f"%{text2}%")))
        else:
            query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text1}%"))
            query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text2}%"))

    elif text1:
        query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text1}%"))

    elif text2:
        query = query.filter(Inscriptions.text_epidoc_form.like(f"%{text2}%"))

    count = query.count()

    if count > 100:
        query = query.limit(100)

    results = query.all()

    return render_template("search/basic_do.html", results=results, count=count)