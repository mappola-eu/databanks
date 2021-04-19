from . import db

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
    object_execution_technique_id = db.Column(db.Integer, db.ForeignKey('object_execution_techniques.id'))
    object_decoration_comment = db.Column(db.Text)
    object_text_layout_comment = db.Column(db.Text)

    text_function_id = db.Column(db.Integer, db.ForeignKey('text_functions.id'))
    text_diplomatic_form = db.Column(db.Text)
    text_interpretative_form = db.Column(db.Text)
    text_metrics_visualised_form = db.Column(db.Text)


    text_apparatus_criticus_comment = db.Column(db.Text)
    general_comment = db.Column(db.Text)
    date = db.Column(db.Text)

    place = db.relationship('Places', backref='inscriptions')
    current_location = db.relationship('CurrentLocations', backref='inscriptions')
    object_type = db.relationship('ObjectTypes', backref='inscriptions')
    object_material = db.relationship('ObjectMaterials', backref='inscriptions')
    object_preservation_state = db.relationship('ObjectPreservationStates', backref='inscriptions')
    object_execution_technique = db.relationship('ObjectExecutionTechniques', backref='inscriptions')


class ObjectTypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

class ObjectMaterials(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

class ObjectPreservationStates(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

class ObjectExecutionTechniques(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

class ObjectDecorationTags(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class TextFunctions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class VerseTimingTypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class Languages(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class CurrentLocations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class Places(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class Provinces(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleGenders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleAges(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleAgeExpressions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))

class PeopleAgePrecision(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleOrigins(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleLegalStatus(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleRanks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class PeopleProfessions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class DatingCriteria(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    
class VerseTypes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    parent_verse_type_id = db.Column(db.Integer, db.ForeignKey('verse_types.id'))

class Translations(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    translated_form = db.Column(db.Text)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    link_to_published_transition = db.Column(db.Text)

class Publications(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    reference_comment = db.Column(db.Text)

class People(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    reference_link = db.Column(db.Text)
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))
    people_gender_id = db.Column(db.Integer, db.ForeignKey('people_genders.id'))