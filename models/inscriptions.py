from . import db
from sqlalchemy import event
from ..linkage import LINKERS
from ..linkage.epidoc import *
import json
import re, sys

VERY_LARGE_NUMBER = sys.maxsize

with open("models/definition.json", "r") as f:
    defn = json.load(f)

inscription_decoration_tag_assoc = db.Table(
    'inscription_decoration_tag_assoc',
    db.Column(
        'inscription_id',
        db.Integer(),
        db.ForeignKey('inscriptions.id')),
    db.Column(
        'object_decoration_tag_id',
        db.Integer(),
        db.ForeignKey('object_decoration_tags.id')))

inscription_language_assoc = db.Table(
    'inscription_language_assoc',
    db.Column(
        'inscription_id',
        db.Integer(),
        db.ForeignKey('inscriptions.id')),
    db.Column(
        'language_id',
        db.Integer(),
        db.ForeignKey('languages.id')))


inscription_dating_criterion_assoc = db.Table(
    'inscription_dating_criterion_assoc',
    db.Column(
        'inscription_id',
        db.Integer(),
        db.ForeignKey('inscriptions.id')),
    db.Column(
        'dating_criterion_id',
        db.Integer(),
        db.ForeignKey('dating_criteria.id')))


inscription_verse_type_assoc = db.Table(
    'inscription_verse_type_assoc',
    db.Column(
        'inscription_id',
        db.Integer(),
        db.ForeignKey('inscriptions.id')),
    db.Column(
        'verse_type_id',
        db.Integer(),
        db.ForeignKey('verse_types.id')),
    db.Column(
        'verse_timing_type_id',
        db.Integer(),
        db.ForeignKey('verse_timing_types.id')))

inscription_text_layout_tag_assoc = db.Table(
    'inscription_text_layout_tag_assoc',
    db.Column(
        'inscription_id',
        db.Integer(),
        db.ForeignKey('inscriptions.id')),
    db.Column(
        'text_layout_tag_id',
        db.Integer(),
        db.ForeignKey('text_layout_tags.id')))

inscription_people_assoc = db.Table(
    'inscription_people_assoc',
    db.Column(
        'inscription_id',
        db.Integer(),
        db.ForeignKey('inscriptions.id')),
    db.Column(
        'people_id',
        db.Integer(),
        db.ForeignKey('people.id')))


class Inscriptions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(180))
    trismegistos_nr = db.Column(db.String(40))

    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    find_comment = db.Column(db.Text)
    coordinates_long = db.Column(db.Float())
    coordinates_lat = db.Column(db.Float())
    current_location_id = db.Column(
        db.Integer, db.ForeignKey('current_locations.id'))
    current_location_inventory = db.Column(db.String(80))
    current_location_details = db.Column(db.Text)
    

    object_type_id = db.Column(db.Integer, db.ForeignKey('object_types.id'))
    object_material_id = db.Column(
        db.Integer, db.ForeignKey('object_materials.id'))
    object_preservation_state_id = db.Column(
        db.Integer, db.ForeignKey('object_preservation_states.id'))
    object_dim_height = db.Column(db.Float)  # Y
    object_dim_width = db.Column(db.Float)  # X
    object_dim_depth = db.Column(db.Float)  # Z
    object_execution_technique_id = db.Column(
        db.Integer, db.ForeignKey('object_execution_techniques.id'))
    object_decoration_comment = db.Column(db.Text)
    object_text_layout_comment = db.Column(db.Text)
    object_text_layout_tags = db.relationship(
        'TextLayoutTags', secondary=inscription_text_layout_tag_assoc, backref='inscriptions')

    letter_size_min = db.Column(db.Float)
    letter_size_max = db.Column(db.Float)

    text_function_id = db.Column(
        db.Integer, db.ForeignKey('text_functions.id'))
    text_epidoc_form = db.Column(db.Text)

    text_interpretative_cached = db.Column(db.Text)
    text_diplomatic_cached = db.Column(db.Text)
    text_metrics_visualised_cached = db.Column(db.Text)

    main_translation = db.Column(db.Text)
    translation_author = db.Column(db.String(150))

    layout_conditioned_by_language = db.Column(db.Boolean)

    text_apparatus_criticus_comment = db.Column(db.Text)
    general_comment = db.Column(db.Text)
    date_begin = db.Column(db.Integer)
    date_end = db.Column(db.Integer)

    religion_id = db.Column(db.Integer, db.ForeignKey('religions.id'))

    place = db.relationship('Places', backref='inscriptions')
    current_location = db.relationship(
        'CurrentLocations', backref='inscriptions')
    object_type = db.relationship('ObjectTypes', backref='inscriptions')
    object_material = db.relationship(
        'ObjectMaterials', backref='inscriptions')
    object_preservation_state = db.relationship(
        'ObjectPreservationStates', backref='inscriptions')
    object_execution_technique = db.relationship(
        'ObjectExecutionTechniques', backref='inscriptions')
    text_function = db.relationship('TextFunctions', backref='inscriptions')
    religion = db.relationship('Religions', backref='inscriptions')

    languages = db.relationship(
        'Languages', secondary=inscription_language_assoc, backref='inscriptions')
    decoration_tags = db.relationship(
        'ObjectDecorationTags', secondary=inscription_decoration_tag_assoc, backref='inscriptions')
    dating_criteria = db.relationship(
        'DatingCriteria', secondary=inscription_dating_criterion_assoc, backref='inscriptions')
    verse_types = db.relationship(
        'VerseTypes', secondary=inscription_verse_type_assoc, backref='inscriptions')
    people = db.relationship(
        'People', secondary=inscription_people_assoc, backref='inscriptions')

    translations = db.relationship('Translations', backref='inscription')

    have_squeeze = db.Column(db.Boolean)

    last_updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    last_updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_updated_by = db.relationship('User')
    work_status_id = db.Column(db.Integer, db.ForeignKey('work_status.id'))
    work_status = db.relationship('WorkStatus')

    def long_id(self):
        if self.id is not None:
            return "MPL" + str(self.id).zfill(5)
        else:
            return "MPL?????"

    def text_diplomatic(self):
        base = self.text_diplomatic_cached
        base = base.replace("U", "V")
        base = re.subn("\[.*\..*\]", lambda s: s[0].replace(".", ""), base)[0]

        while "=<br" in base or "= <br" in base:
            base = base.replace("=<br", "<br")
            base = base.replace("= <br", "<br")

        return base

    def text_interpretative(self):
        return self.text_interpretative_cached.split('~~~APP BELOW~~~')[0]

    def text_with_metrics_visualised(self):
        return self.text_metrics_visualised_cached

    def work_status_str(self):
        return '' if not self.work_status else self.work_status.title

    def auto_apparatus(self):
        itt = self.text_interpretative_cached.split('~~~APP BELOW~~~')

        if len(itt) == 1:
            return ""

        return itt[1]

    def update_str(self):
        if self.last_updated_at is None:
            return "never (either you are creating this inscription right now or this is an error)."

        if self.last_updated_by is None:
            return self.last_updated_at.strftime("%Y-%m-%d") + ", by anon"
        else:
            return self.last_updated_at.strftime("%Y-%m-%d") + ", by " + self.last_updated_by.full_name


class WorkStatus(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class ObjectTypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class ObjectMaterials(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class ObjectPreservationStates(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class ObjectExecutionTechniques(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class ObjectDecorationTags(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

    parent_object_decoration_tag_id = db.Column(
        db.Integer, db.ForeignKey('object_decoration_tags.id'))
    parent_object_decoration_tag = db.relationship(
        'ObjectDecorationTags', remote_side=[id])
    enum_lod = db.Column(db.String(150))

    def parent_object_decoration_tag_name(self):
        if self.parent_object_decoration_tag is not None:
            return self.parent_object_decoration_tag.title
        else:
            return self.title


class TextFunctions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class VerseTimingTypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class Languages(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class CurrentLocations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class Places(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

    ancient_name = db.Column(db.String(90))
    modern_name = db.Column(db.String(90))

    coordinates_long = db.Column(db.Float())
    coordinates_lat = db.Column(db.Float())

    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    province = db.relationship('Provinces', backref='places')
    modern_region_id = db.Column(
        db.Integer, db.ForeignKey('modern_regions.id'))
    modern_region = db.relationship('ModernRegions', backref='places')

    pleiades_id = db.Column(db.Integer())
    geonames_id = db.Column(db.Integer())
    enum_lod = db.Column(db.String(150))

    def modern_region_name(self):
        if not self.modern_region:
            return '-'

        return f"{self.modern_region.title} ({self.modern_region.modern_state_name()})"


class Provinces(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class ModernRegions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))

    state_id = db.Column(db.Integer, db.ForeignKey('modern_states.id'))
    state = db.relationship('ModernStates', backref='modern_regions')

    def modern_state_name(self):
        return self.state.title if self.state else '-'


class ModernStates(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleGenders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleAges(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleAgeExpressions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleAgePrecision(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleOrigins(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleLegalStatus(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleRanks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class PeopleProfessions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class DatingCriteria(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class VerseTypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    parent_verse_type_id = db.Column(
        db.Integer, db.ForeignKey('verse_types.id'))
    parent_verse_type = db.relationship('VerseTypes', remote_side=[id])
    enum_lod = db.Column(db.String(150))

    def parent_verse_name(self):
        if self.parent_verse_type_id is not None:
            return self.parent_verse_type.title
        else:
            return self.title


class Translations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    translated_form = db.Column(db.Text)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    link_to_published_translation = db.Column(db.Text)

    language = db.relationship('Languages')

    def language_title(self):
        return self.language.title

    def display(self):
        return self.link_to_published_translation + " (" + self.language_title() + ")"


class TextLayoutTags(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class Publications(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    reference_comment = db.Column(db.Text)
    zotero_item_id = db.Column(db.String(20))

    inscription = db.relationship('Inscriptions', backref='publications')

    order_number = db.Column(db.Integer)

    def display(self):
        return self.reference_comment #+ " (" + self.zotero_item_id + ")"


class People(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    reference_link = db.Column(db.Text)
    name = db.Column(db.Text)
    people_gender_id = db.Column(
        db.Integer, db.ForeignKey('people_genders.id'))
    people_age_id = db.Column(db.Integer, db.ForeignKey('people_ages.id'))
    people_age_expression_id = db.Column(
        db.Integer, db.ForeignKey('people_age_expressions.id'))
    people_age_precision_id = db.Column(
        db.Integer, db.ForeignKey('people_age_precision.id'))
    people_origin_id = db.Column(
        db.Integer, db.ForeignKey('people_origins.id'))
    people_legal_status_id = db.Column(
        db.Integer, db.ForeignKey('people_legal_status.id'))
    people_rank_id = db.Column(db.Integer, db.ForeignKey('people_ranks.id'))
    people_profession_id = db.Column(
        db.Integer, db.ForeignKey('people_professions.id'))

    gender = db.relationship('PeopleGenders', backref='people')
    age = db.relationship('PeopleAges', backref='people')
    age_expression = db.relationship('PeopleAgeExpressions', backref='people')
    age_precision = db.relationship('PeopleAgePrecision', backref='people')
    origin = db.relationship('PeopleOrigins', backref='people')
    legal_status = db.relationship('PeopleLegalStatus', backref='people')
    rank = db.relationship('PeopleRanks', backref='people')
    profession = db.relationship('PeopleProfessions', backref='people')


class Religions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


def get_enum(enum):
    if enum in defn["classes"]:
        return eval(enum)

    else:
        raise NameError("Enumeration not found: ", enum)


def get_rel(rel):
    if rel in defn["relations"].keys():
        return eval(rel)

    else:
        raise NameError("Relation not found: ", rel)


def get_defn(enum, scope="display"):
    if enum in defn["classes"] or enum in defn["relations"].keys():
        if scope in ["display", "summary"]:
            if enum in defn[scope].keys():
                return defn[scope][enum]
            elif enum in defn["enums"]:
                return defn[scope]["_enums"]
            else:
                raise NameError("Enumeration not found in scope: ", enum)
        else:
            raise NameError("Scope not found: ", scope)
    else:
        raise NameError("Enumeration not found: ", enum)


def get_rel_defn(rel):
    if rel in defn["relations"].keys():
        return defn["relations"][rel]

    else:
        raise NameError("Relation not found: ", rel)


def defn_parse_raw(code, item, **args):
    on, key = code.split("#")
    if on == "obj":
        on_obj = item
    elif on in args.keys():
        on_obj = args[on]
    else:
        return ""

    if key == "":
        return on_obj

    exec_func = key.endswith("()")
    if exec_func:
        key = key[:-2]

    if hasattr(on_obj, key):
        key_obj = getattr(on_obj, key)
        if exec_func:
            key_obj = key_obj()
        return key_obj
    else:
        return ""


def defn_parse(*args, **kwargs):
    return str(defn_parse_raw(*args, **kwargs))


def render_column(item, col):
    linkage = None
    if 'ext_linkage' in col:
        linker = LINKERS[col['ext_linkage']]
        if col['type'] not in ("reference_list", "reference_complex", "reference_func", "dimension"):
            linkage = linker.pair(item)
    else:
        linker = LINKERS['null']

    if col["type"] in ["input", "text", "numeric_input"]:
        if hasattr(item, col["column"]):
            return ((getattr(item, col["column"]) or ""), linkage)
    elif col["type"] == "boolean_input":
        if hasattr(item, col["column"]):
            return (getattr(item, col["column"]), linkage)
    elif col["type"] == "call":
        return (defn_parse(col["column"], item), linkage)
    elif col["type"] == "dimension":
        width, height, depth = getattr(item, col["column"][0]), getattr(item, col["column"][1]), \
            getattr(item, col["column"][2])
        return ([width, height, depth], linkage)
    elif col["type"] == "reference":
        if hasattr(item, col["column"]) and (column_value := getattr(item, col["column"])) is not None:
            return (column_value.title, linkage)
    elif col["type"] == "reference_list":
        if hasattr(item, col["column"]):
            return [(i.title, linker.link(i)) for i in getattr(item, col["column"])]
    elif col["type"] == "reference_complex":
        if hasattr(item, col["column"]):
            base = getattr(item, col["column"])

            if 'order' in col:
                base = sorted(base, key=lambda i: getattr(i, col["order"]) or VERY_LARGE_NUMBER)

            return [(getattr(i, col["render"]), linker.link(i)) for i in base]
    elif col["type"] == "reference_func":
        if hasattr(item, col["column"]):
            base = getattr(item, col["column"])

            if 'order' in col:
                base = sorted(base, key=lambda i: getattr(i, col["order"]) or VERY_LARGE_NUMBER)

            return [(getattr(i, col["render"])(), linker.link(i)) for i in base]
    return ("", linkage)


def defn_snippet(snippet, *args, **kwargs):
    return re.sub(r"\$\{([a-zA-Z]+\#[a-zA-Z]+(?:\(\))?)\}",
                  lambda mo: defn_parse(mo.group(1), *args, **kwargs),
                  snippet)


def get_enum_with_grouping(refersto, grouping):
    data = get_enum(refersto).query.all()

    groups = {}

    for e in data:
        group = getattr(e, grouping['attribute'])

        if group is None and "id_if_equal" in grouping:
            group = e.id

        if group in groups:
            groups[group] += [e]
        else:
            groups[group] = [e]

    out_data = []
    for gv in groups.values():
        gv = sorted(gv, key = lambda x: x.title)
        out_data += [{
            "label": defn_parse_raw(grouping['representation'], gv[0]),
            "entities": gv
        }]

    out_data = sorted(out_data, key = lambda x: x['label'])

    return out_data


def postproc(data, type_):
    if 'post_process' not in type_:
        return data

    elif type_['post_process'] == 'date':
        if not data[0]:
            return '', data[1]
        elif type(data[0]) == str:
            data = int(data[0]), data[1]

        if data[0] < 0:
            return f"{-data[0]} BC", data[1]
        else:
            return f"{data[0]} AD", data[1]

    elif type_['post_process'] == 'bool':
        if data[0]:
            return "yes", data[1]
        else:
            return "no", data[1]

    return data
