from . import db
from ..linkage import LINKERS
from ..linkage.epidoc import *
import json, re

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
    current_location_id = db.Column(db.Integer, db.ForeignKey('current_locations.id'))

    object_type_id = db.Column(db.Integer, db.ForeignKey('object_types.id'))
    object_material_id = db.Column(db.Integer, db.ForeignKey('object_materials.id'))
    object_preservation_state_id = db.Column(db.Integer, db.ForeignKey('object_preservation_states.id'))
    object_dim_height = db.Column(db.Float) # Y
    object_dim_width = db.Column(db.Float) # X
    object_dim_depth = db.Column(db.Float) # Z
    object_execution_technique_id = db.Column(db.Integer, db.ForeignKey('object_execution_techniques.id'))
    object_decoration_comment = db.Column(db.Text)
    object_text_layout_comment = db.Column(db.Text)

    text_function_id = db.Column(db.Integer, db.ForeignKey('text_functions.id'))
    text_epidoc_form = db.Column(db.Text)


    text_apparatus_criticus_comment = db.Column(db.Text)
    general_comment = db.Column(db.Text)
    date = db.Column(db.Text)

    place = db.relationship('Places', backref='inscriptions')
    current_location = db.relationship('CurrentLocations', backref='inscriptions')
    object_type = db.relationship('ObjectTypes', backref='inscriptions')
    object_material = db.relationship('ObjectMaterials', backref='inscriptions')
    object_preservation_state = db.relationship('ObjectPreservationStates', backref='inscriptions')
    object_execution_technique = db.relationship('ObjectExecutionTechniques', backref='inscriptions')
    text_function = db.relationship('TextFunctions', backref='inscriptions')

    languages = db.relationship('Languages', secondary=inscription_language_assoc, backref='inscriptions')
    decoration_tags = db.relationship('ObjectDecorationTags', secondary=inscription_decoration_tag_assoc, backref='inscriptions')
    dating_criteria = db.relationship('DatingCriteria', secondary=inscription_dating_criterion_assoc, backref='inscriptions')
    verse_types = db.relationship('VerseTypes', secondary=inscription_verse_type_assoc, backref='inscriptions')
    people = db.relationship('People', secondary=inscription_people_assoc, backref='inscriptions')

    translations = db.relationship('Translations', backref='inscription')

    def long_id(self):
        if self.id is not None:
            return "MPL" + str(self.id).zfill(5)
        else:
            return "MPL?????"

    def text_diplomatic(self):
        return epidoc_to_diplomatic(self.text_epidoc_form)
    
    def text_interpretative(self):
        return "[[I]]"
    
    def text_with_metrics_visualised(self):
        return "[[MV]]"


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
    enum_lod = db.Column(db.String(150))
    
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
    pleiades_id = db.Column(db.Integer())
    enum_lod = db.Column(db.String(150))
    
class Provinces(db.Model):
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
    parent_verse_type_id = db.Column(db.Integer, db.ForeignKey('verse_types.id'))
    enum_lod = db.Column(db.String(150))

class Translations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    translated_form = db.Column(db.Text)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    link_to_published_translation = db.Column(db.Text)

    language = db.relationship('Languages')

    def language_title(self):
        return self.language.title

    def excerpt(self):
        if len(self.translated_form) > 150:
            return self.translated_form[:100] + "..."
        else:
            return self.translated_form

class Publications(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    reference_comment = db.Column(db.Text)
    zotero_item_id = db.Column(db.String(20))

    inscription = db.relationship('Inscriptions', backref='publications')

    def display(self):
        return self.reference_comment + " (" + self.zotero_item_id + ")"

class People(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    reference_link = db.Column(db.Text)
    name = db.Column(db.Text)
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_age_id = db.Column(db.Integer, db.ForeignKey('people_ages.id'))
    people_age_expression_id = db.Column(db.Integer, db.ForeignKey('people_age_expressions.id'))
    people_age_precision_id = db.Column(db.Integer, db.ForeignKey('people_age_precision.id'))
    people_origin_id = db.Column(db.Integer, db.ForeignKey('people_origins.id'))
    people_legal_status_id = db.Column(db.Integer, db.ForeignKey('people_legal_status.id'))
    people_rank_id = db.Column(db.Integer, db.ForeignKey('people_ranks.id'))
    people_profession_id = db.Column(db.Integer, db.ForeignKey('people_professions.id'))

    gender = db.relationship('PeopleGenders', backref='people')
    age = db.relationship('PeopleAges', backref='people')
    age_expression = db.relationship('PeopleAgeExpressions', backref='people')
    age_precision = db.relationship('PeopleAgePrecision', backref='people')
    origin = db.relationship('PeopleOrigins', backref='people')
    legal_status = db.relationship('PeopleLegalStatus', backref='people')
    rank = db.relationship('PeopleRanks', backref='people')
    profession = db.relationship('PeopleProfessions', backref='people')

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
    
    exec_func =  key.endswith("()")
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
        if col['type'] not in ("reference_list", "reference_complex", "reference_func"):
            linkage = linker.link(item)
    else:
        linker = LINKERS['null']

    if col["type"] in ["input", "text"]:
        if hasattr(item, col["column"]):
            return ((getattr(item, col["column"]) or ""), linkage)
    elif col["type"] == "call":
        return (defn_parse(col["column"], item), linkage)
    elif col["type"] == "dimension":
        width, height, depth = getattr(item, col["column"][0]), getattr(item, col["column"][1]), \
                                   getattr(item, col["column"][2])
        return ([width, height, depth], linkage)
    elif col["type"] == "reference":
        if hasattr(item, col["column"]):
            return (getattr(item, col["column"]).title, linkage)
    elif col["type"] == "reference_list":
        if hasattr(item, col["column"]):
            return [(i.title, linker.link(i)) for i in getattr(item, col["column"])]
    elif col["type"] == "reference_complex":
        if hasattr(item, col["column"]):
            return [(getattr(i, col["render"]), linker.link(i)) for i in getattr(item, col["column"])]
    elif col["type"] == "reference_func":
        if hasattr(item, col["column"]):
            return [(getattr(i, col["render"])(), linker.link(i)) for i in getattr(item, col["column"])]
    return ("", linkage)

def defn_snippet(snippet, *args, **kwargs):
    return re.sub(r"\$\{([a-zA-Z]+\#[a-zA-Z]+(?:\(\))?)\}",
                  lambda mo: defn_parse(mo.group(1), *args, **kwargs),
                  snippet)