from flask import *
from ..models import db, get_enum, Inscriptions, Places, VerseTypes, Publications, inscriptions_to_json
from ..config import SETTINGS

from sqlalchemy import select

search = Blueprint('search', __name__)


@search.route("/", methods=["GET"])
def index():
    return redirect(url_for('search.basic'))


@search.route("/basic", methods=["GET"])
def basic():
    return render_template("search/basic.html", get_enum=get_enum)


@search.route("/advanced", methods=["GET"])
def advanced():
    return render_template("search/advanced.html", get_enum=get_enum)


@search.route("/basic/do", methods=["GET"])
def basic_do():
    query = Inscriptions.query.distinct()
    places = Places.query
    places_subquery = False

    query, places, places_subquery = _apply_common_filters(query, places, places_subquery)

    if places_subquery:
        query = query.filter(Inscriptions.place_id.in_(
            [i[0] for i in places.values(Places.id)]))
        
    query = _apply_basic_text_filters(query)

    count = query.count()
    results = query.all()
    mc = inscriptions_to_json(results)

    return render_template("search/do.html", results=results, count=count, mc=mc, origin='basic')


@search.route("/advanced/do", methods=["GET"])
def advanced_do():
    query = Inscriptions.query.distinct()
    places = Places.query
    places_subquery = False

    query, places, places_subquery = _apply_common_filters(query, places, places_subquery)
    query, places, places_subquery = _apply_advanced_filters(query, places, places_subquery)

    if places_subquery:
        query = query.filter(Inscriptions.place_id.in_(
            [i[0] for i in places.values(Places.id)]))
        
    query = _apply_advanced_text_filters(query)

    count = query.count()
    results = query.all()
    mc = inscriptions_to_json(results)

    return render_template("search/do.html", results=results, count=count, mc=mc, origin='advanced')


def _apply_common_filters(query, places, places_subquery):
    if 'mappola_id' in request.values.keys() and (mappola_id := request.values.get('mappola_id')) != '':
        query = query.filter(Inscriptions.id == mappola_id)

    if 'province' in request.values.keys() and (province := request.values.get('province')) != '':
        places = places.filter(Places.province_id == province)
        places_subquery = True

    if 'state' in request.values.keys() and (state := request.values.get('state')) != '':
        places = places.filter(Places.modern_state_id == state)
        places_subquery = True

    if 'date_min' in request.values.keys() and (date_min := request.values.get('date_min')) != '':
        query = query.filter(Inscriptions.date_begin >= date_min)

    if 'date_max' in request.values.keys() and (date_max := request.values.get('date_max')) != '':
        query = query.filter(Inscriptions.date_end <= date_max)

    if 'bibliography' in request.values.keys() and (bibliography := request.values.get('bibliography')) != '':
        bibliography = Publications.query.filter(Publications.reference_comment.like(
            f"%{bibliography}%")).union(Publications.query.filter_by(zotero_item_id=bibliography)).all()
        subquery = None

        for bib in bibliography:
            if subquery is None:
                subquery = Inscriptions.publications.contains(bib)
            else:
                subquery = subquery | Inscriptions.publications.contains(bib)

        query = query.filter(subquery)

    if 'verse_type' in request.values.keys() and (verse_types := request.values.getlist('verse_type')) != ['']:
        not_expanded = []
        searched_verse_types = []

        for verse_type in verse_types:
            verse_type = VerseTypes.query.filter_by(id=verse_type).one()
            not_expanded += [verse_type]

        while len(not_expanded):
            vt = not_expanded.pop()

            if vt in searched_verse_types:
                continue

            searched_verse_types.append(vt)
            not_expanded += vt.children

        subquery = None

        for vt in searched_verse_types:
            if subquery is None:
                subquery = Inscriptions.verse_types.contains(vt)
            else:
                subquery = subquery | Inscriptions.verse_types.contains(vt)

        query = query.filter(subquery)

    return query, places, places_subquery



def _apply_basic_text_filters(query):
    if 'text1' in request.values.keys() and (text1 := request.values.get('text1')) != '' and \
            'text2' in request.values.keys() and (text2 := request.values.get('text2')) != '':

        if request.values.get('text_conj', 'AND') == 'OR':
            query = query.filter(Inscriptions.inscription_search_body_cached.ilike(f"%{text1}%")) \
                .union(query.filter(Inscriptions.inscription_search_body_cached.ilike(f"%{text2}%")))
        elif request.values.get('text_conj', 'AND') == 'AND NOT':
            query = query.filter(
                Inscriptions.inscription_search_body_cached.ilike(f"%{text1}%"))
            query = query.filter(
                Inscriptions.inscription_search_body_cached.notlike(f"%{text2}%"))
        else:
            query = query.filter(
                Inscriptions.inscription_search_body_cached.ilike(f"%{text1}%"))
            query = query.filter(
                Inscriptions.inscription_search_body_cached.ilike(f"%{text2}%"))

    elif 'text1' in request.values.keys() and (text1 := request.values.get('text1')) != '':
        query = query.filter(
            Inscriptions.inscription_search_body_cached.ilike(f"%{text1}%"))

    elif 'text2' in request.values.keys() and (text2 := request.values.get('text2')) != '':
        query = query.filter(
            Inscriptions.inscription_search_body_cached.ilike(f"%{text2}%"))

    if 'ft' in request.values.keys() and (ft := request.values.get('ft')) != '':
        query = query.filter(
            Inscriptions.full_text_cached.like(f"%{ft}%"))

    return query


def _apply_advanced_filters(query, places, places_subquery):

    if 'find_place' in request.values.keys() and (find_place := request.values.get('find_place')) != '':
        places = places.filter(Places.id == find_place)
        places_subquery = True
    
    if 'find_context' in request.values.keys() and (find_context := request.values.get('find_context')) != '':
        query = query.filter(Inscriptions.find_comment.ilike(f"%{find_context}%"))

    if 'current_location' in request.values.keys() and (cur_loc := request.values.get('current_location')) != '':
        cur_loc = get_enum('CurrentLocations').query.get(cur_loc)
        query = query.filter(Inscriptions.current_location == cur_loc)

    if 'object_type' in request.values.keys() and (object_type := request.values.get('object_type')) != '':
        object_type = get_enum('ObjectTypes').query.get(object_type)
        query = query.filter(Inscriptions.object_type == object_type)
    
    if 'object_material' in request.values.keys() and (object_material := request.values.get('object_material')) != '':
        object_material = get_enum('ObjectMaterials').query.get(object_material)
        query = query.filter(Inscriptions.object_material == object_material)

    return query, places, places_subquery


def _apply_advanced_text_filters(query):
    if 'ft' in request.values.keys() and (ft := request.values.get('ft')) != '':
        query = query.filter(
            Inscriptions.full_text_cached.like(f"%{ft}%"))

    return query