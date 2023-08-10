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

    if 'verse_type' in request.values.keys() and (verse_type := request.values.get('verse_type')) != '':
        verse_type = VerseTypes.query.filter_by(id=verse_type).one()
        not_expanded = [verse_type]
        searched_verse_types = []

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

    if 'bibliography' in request.values.keys() and (bibliography := request.values.get('bibliography')) != '':
        print(bibliography)
        bibliography = Publications.query.filter(Publications.reference_comment.like(
            f"%{bibliography}%")).union(Publications.query.filter_by(zotero_item_id=bibliography)).all()
        subquery = None

        for bib in bibliography:
            if subquery is None:
                subquery = Inscriptions.publications.contains(bib)
            else:
                subquery = subquery | Inscriptions.publications.contains(bib)

        query = query.filter(subquery)

    if places_subquery:
        query = query.filter(Inscriptions.place_id.in_(
            [i[0] for i in places.values(Places.id)]))

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
    
    count = query.count()

    # if count > 100:
    #     query = query.limit(100)

    results = query.all()

    mc = inscriptions_to_json(results)

    return render_template("search/basic_do.html", results=results, count=count, mc=mc)
