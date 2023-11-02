from flask import *
from ..models import db, get_enum, Inscriptions, Places, VerseTypes, Publications, People, ObjectDecorationTags, inscription_decoration_tag_assoc, inscriptions_to_json
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

    query, places, places_subquery = _apply_common_filters(
        query, places, places_subquery)

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

    query, places, places_subquery = _apply_common_filters(
        query, places, places_subquery)
    query, places, places_subquery = _apply_advanced_filters(
        query, places, places_subquery)

    if places_subquery:
        query = query.filter(Inscriptions.place_id.in_(
            [i[0] for i in places.values(Places.id)]))

    query = _apply_advanced_text_filters(query)
    query = _apply_advanced_people_filters(query)

    print(query)

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
        query = query.filter(
            Inscriptions.find_comment.ilike(f"%{find_context}%"))

    if 'current_location' in request.values.keys() and (cur_loc := request.values.get('current_location')) != '':
        cur_loc = get_enum('CurrentLocations').query.get(cur_loc)
        query = query.filter(Inscriptions.current_location == cur_loc)

    if 'object_type' in request.values.keys() and (object_type := request.values.get('object_type')) != '':
        object_type = get_enum('ObjectTypes').query.get(object_type)
        query = query.filter(Inscriptions.object_type == object_type)

    if 'object_material' in request.values.keys() and (object_material := request.values.get('object_material')) != '':
        object_material = get_enum(
            'ObjectMaterials').query.get(object_material)
        query = query.filter(Inscriptions.object_material == object_material)

    if 'object_preservation' in request.values.keys() and (object_preservation := request.values.get('object_preservation')) != '':
        object_preservation = get_enum(
            'ObjectPreservationStates').query.get(object_preservation)
        query = query.filter(
            Inscriptions.object_preservation_state == object_preservation)

    if 'object_execution' in request.values.keys() and (object_execution := request.values.get('object_execution')) != '':
        object_execution = get_enum(
            'ObjectExecutionTechniques').query.get(object_execution)
        query = query.filter(
            Inscriptions.object_execution_technique == object_execution)

    if 'religion' in request.values.keys() and (religion := request.values.get('religion')) != '':
        religion = get_enum('Religions').query.get(religion)
        query = query.filter(Inscriptions.religion == religion)

    if 'rhythmisation' in request.values.keys() and (rhythmisation := request.values.get('rhythmisation')) != '':
        rhythmisation = get_enum('VerseTimingTypes').query.get(rhythmisation)
        query = query.filter(Inscriptions.verse_timing_type == rhythmisation)

    if 'translations' in request.values.keys() and (translations := request.values.get('translations')) != '':
        Translations = get_enum('Translations')
        query_on_inscr = Inscriptions.main_translation.ilike(f"%{translations}%")
        query_on_transl = Translations.link_to_published_translation.ilike(f"%{translations}%")

        translations = Translations.query.filter(query_on_transl).all()

        subquery = query_on_inscr

        for translation in translations:
            subquery = subquery | Inscriptions.translations.contains(translation)

        query = query.filter(subquery)

    if 'decoration_tags' in request.values.keys() and (decoration_tags := request.values.getlist('decoration_tags')) != ['']:
        not_expanded = []
        searched_decoration_tags = []

        for decoration_tag in decoration_tags:
            decoration_tag = ObjectDecorationTags.query.filter_by(
                id=decoration_tag).one()
            not_expanded += [decoration_tag]

        while len(not_expanded):
            dt = not_expanded.pop()

            if dt.id in searched_decoration_tags:
                continue

            searched_decoration_tags.append(dt.id)
            not_expanded += dt.children

        query = query.join(ObjectDecorationTags, Inscriptions.decoration_tags).filter(ObjectDecorationTags.id.in_(searched_decoration_tags))

    if 'layout_tags' in request.values.keys() and (layout_tags := request.values.getlist('layout_tags')) != ['']:
        subquery = None

        for layout_tag in layout_tags:
            layout_tag = get_enum('TextLayoutTags').query.filter_by(
                id=layout_tag).one()

            if subquery is None:
                subquery = Inscriptions.object_text_layout_tags.contains(
                    layout_tag)
            else:
                subquery = subquery & Inscriptions.object_text_layout_tags.contains(
                    layout_tag)

        query = query.filter(subquery)

    if 'function' in request.values.keys() and (function := request.values.get('function')) != '':
        function = get_enum('TextFunctions').query.get(function)
        query = query.filter(Inscriptions.text_function == function)

    if 'languages' in request.values.keys() and (languages := request.values.getlist('languages')) != ['']:
        subquery = None

        for language in languages:
            language = get_enum('Languages').query.filter_by(id=language).one()

            if subquery is None:
                subquery = Inscriptions.languages.contains(language)
            else:
                subquery = subquery & Inscriptions.languages.contains(language)

        query = query.filter(subquery)

    return query, places, places_subquery


def _apply_advanced_text_filters(query):
    true_query = Inscriptions.id >= -1
    false_query = Inscriptions.id <= -1

    text11 = request.values.get('text11')
    text12 = request.values.get('text12')
    text1_conj = request.values.get('text1_conj').upper()
    text1_query = None

    text21 = request.values.get('text21')
    text22 = request.values.get('text22')
    text2_conj = request.values.get('text2_conj').upper()
    text2_query = None

    text31 = request.values.get('text31')
    text32 = request.values.get('text32')
    text3_conj = request.values.get('text3_conj').upper()
    text3_query = None

    text_method = request.values.get('text_method').upper()

    if text11 != '' or text12 != '':
        text11_query = text12_query = None

        if text11 != '':
            text11_query = Inscriptions.inscription_search_body_cached.ilike(
                f"%{text11}%")

        if text12 != '':
            text12_query = Inscriptions.inscription_search_body_cached.ilike(
                f"%{text12}%")

        if text1_conj == 'AND':
            text1_query = true_query
            if text11_query is not None:
                text1_query = text1_query & text11_query
            if text12_query is not None:
                text1_query = text1_query & text12_query
        elif text1_conj == 'OR':
            text1_query = false_query
            if text11_query is not None:
                text1_query = text1_query | text11_query
            if text12_query is not None:
                text1_query = text1_query | text12_query
        elif text1_conj == 'AND NOT':
            text1_query = true_query
            if text11_query is not None:
                text1_query = text1_query & text11_query
            if text12_query is not None:
                text1_query = text1_query & ~text12_query

    if text21 != '' or text22 != '':
        text21_query = text22_query = None

        if text21 != '':
            text21_query = Inscriptions.inscription_search_body_cached.ilike(
                f"%{text21}%")

        if text22 != '':
            text22_query = Inscriptions.inscription_search_body_cached.ilike(
                f"%{text22}%")

        if text2_conj == 'AND':
            text2_query = true_query
            if text21_query is not None:
                text2_query = text2_query & text21_query
            if text22_query is not None:
                text2_query = text2_query & text22_query
        elif text2_conj == 'OR':
            text2_query = false_query
            if text21_query is not None:
                text2_query = text2_query | text21_query
            if text22_query is not None:
                text2_query = text2_query | text22_query
        elif text2_conj == 'AND NOT':
            text2_query = true_query
            if text21_query is not None:
                text2_query = text2_query & text21_query
            if text22_query is not None:
                text2_query = text2_query & ~text22_query

    if text31 != '' or text32 != '':
        text31_query = text32_query = None

        if text31 != '':
            text31_query = Inscriptions.inscription_search_body_cached.ilike(
                f"%{text31}%")

        if text32 != '':
            text32_query = Inscriptions.inscription_search_body_cached.ilike(
                f"%{text32}%")

        if text3_conj == 'AND':
            text3_query = true_query
            if text31_query is not None:
                text3_query = text3_query & text31_query
            if text32_query is not None:
                text3_query = text3_query & text32_query
        elif text3_conj == 'OR':
            text3_query = false_query
            if text31_query is not None:
                text3_query = text3_query | text31_query
            if text32_query is not None:
                text3_query = text3_query | text32_query
        elif text3_conj == 'AND NOT':
            text3_query = true_query
            if text31_query is not None:
                text3_query = text3_query & text31_query
            if text32_query is not None:
                text3_query = text3_query & ~text32_query

    if text_method == "ALL OF":
        subquery = true_query
        if text1_query is not None:
            subquery = subquery & text1_query
        if text2_query is not None:
            subquery = subquery & text2_query
        if text3_query is not None:
            subquery = subquery & text3_query
        query = query.filter(subquery)
    elif text_method == "ONE OF":
        subquery = false_query
        if text1_query is not None:
            subquery = subquery | text1_query
        if text2_query is not None:
            subquery = subquery | text2_query
        if text3_query is not None:
            subquery = subquery | text3_query
        query = query.filter(subquery)

    if 'ft' in request.values.keys() and (ft := request.values.get('ft')) != '':
        query = query.filter(
            Inscriptions.full_text_cached.like(f"%{ft}%"))

    return query


def _apply_advanced_people_filters(query):
    people = People.query
    people_subquery = False

    if 'pname' in request.values.keys() and (pname := request.values.get('pname')) != '':
        people = people.filter(People.name.ilike(f"%{pname}%"))
        people_subquery = True

    for key, obj, crit in [['pgender', 'PeopleGenders', People.gender],
                           ['page', 'PeopleAges', People.age],
                           ['pageexpr', 'PeopleAgeExpressions', People.age_expression],
                           ['pageprec', 'PeopleAgePrecision', People.age_precision],
                           ['porigins', 'PeopleOrigins', People.origin],
                           ['plegal', 'PeopleLegalStatus', People.legal_status],
                           ['prank', 'PeopleRanks', People.rank],
                           ['pprofession', 'PeopleProfessions', People.profession],
                           ['prole', 'PeopleRoles', People.role]]:   
        if key in request.values.keys() and (values := request.values.getlist(key)) != ['']:
            subquery = None
            for value in values:
                value = get_enum(obj).query.filter_by(id=value).one()
                if subquery is None:
                    subquery = crit == value
                else:
                    subquery = subquery | (crit == value)
            people = people.filter(subquery)
            people_subquery = True

    if people_subquery:
        subquery = None
        for person in people.all():
            if subquery is None:
                subquery = Inscriptions.people.contains(person)
            else:
                subquery = subquery | Inscriptions.people.contains(person)

        query = query.filter(subquery)
    
    return query