from . import db
from sqlalchemy import event
from ..linkage import LINKERS
from ..linkage.epidoc import *
import json
import re
import sys
import flask
from flask import Markup
from lxml import html

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
    inscription_search_body_cached = db.Column(db.Text)
    full_text_cached = db.Column(db.Text)

    verse_timing_type_id = db.Column(
        db.Integer, db.ForeignKey('verse_timing_types.id'))

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
    verse_timing_type = db.relationship(
        'VerseTimingTypes', backref='inscriptions')

    languages = db.relationship(
        'Languages', secondary=inscription_language_assoc, backref='inscriptions')
    decoration_tags = db.relationship(
        'ObjectDecorationTags', secondary=inscription_decoration_tag_assoc, backref='inscriptions')
    dating_criteria = db.relationship(
        'DatingCriteria', secondary=inscription_dating_criterion_assoc, backref='inscriptions')
    verse_types = db.relationship(
        'VerseTypes', secondary=inscription_verse_type_assoc, backref='inscriptions')

    translations = db.relationship('Translations', backref='inscription')
    images = db.relationship('Images', backref='inscription')
    people = db.relationship('People', backref='inscription')

    have_squeeze = db.Column(db.Boolean)

    last_updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    last_updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_updated_by = db.relationship('User')
    work_status_id = db.Column(db.Integer, db.ForeignKey('work_status.id'))
    work_status = db.relationship('WorkStatus')

    def make_searchable_inscription_cache(self):
        text_base = self.text_epidoc_form + "\n\n"

        tree = html.fromstring(self.text_interpretative())
        text = tree.text_content().strip() + "\n\n"

        text += re.subn(r"\(.*?\)|\⸢.*?\⸣", "", text.strip())[0] + "\n\n"
        text += re.subn(r" *\((.*?)\) *| *\⸢(.*?)\⸣ *", r"\1\2", text.strip())[0] + "\n\n"

        tree = html.fromstring(self.text_diplomatic())
        text += tree.text_content().strip()

        if self.text_metrics_visualised_cached:
            tree = html.fromstring(self.text_with_metrics_visualised())
            text += "\n\n" + tree.text_content().strip()

        text = re.subn(r"[0-9]+", "", text)[0]

        while " (" in text:
            text = text.replace(" (", "(")
        while " ." in text:
            text = text.replace(" .", ".")
        while " ," in text:
            text = text.replace(" ,", ",")
        while "  " in text:
            text = text.replace("  ", " ")

        text += text.replace(" ", "")
        text += text.replace("-", "")
        
        self.inscription_search_body_cached = (text_base + text).upper()

        return self.inscription_search_body_cached
    
    def make_fulltext_cache(self):
        def _defaults(c):
            if c:
                return c.title

            return ''

        ft_base = [self.title]
        ft_base.append(self.make_searchable_inscription_cache())
        ft_base.append(self.long_id())
        ft_base.append(_defaults(self.object_type))
        ft_base.append(_defaults(self.object_material))
        ft_base.append(_defaults(self.object_preservation_state))
        ft_base.append(_defaults(self.object_execution_technique))
        ft_base.append(self.object_decoration_comment)
        ft_base.append(self.object_text_layout_comment)
        ft_base.append(_defaults(self.text_function))
        ft_base.append(_defaults(self.verse_timing_type))
        ft_base.append(self.main_translation)
        ft_base.append(self.translation_author)
        ft_base.append(self.text_apparatus_criticus_comment)
        ft_base.append(self.general_comment)
        ft_base.append(self.current_location_inventory)
        ft_base.append(_defaults(self.religion))

        for tag in self.object_text_layout_tags:
            ft_base.append(tag.title)
        
        for tag in self.decoration_tags:
            ft_base.append(tag.title)
        
        for crit in self.dating_criteria:
            ft_base.append(crit.title)
        
        for tp in self.verse_types:
            ft_base.append(tp.title)
        
        for t in self.translations:
            ft_base.append(t.display())
        
        try:
            ft_base = [i for i in ft_base if i is not None and len(i)]
        except:
            print(ft_base)

        self.full_text_cached = "\n".join(ft_base).upper()

        return self.full_text_cached

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

    def text_only_preview(self):
        tree = html.fromstring(self.text_interpretative())
        text = tree.text_content().strip()

        if len(text) < 50:
            return text
        else:
            return text[:50] + "…"

    def work_status_str(self):
        return '' if not self.work_status else self.work_status.title

    def auto_apparatus(self):
        itt = self.text_interpretative_cached.split('~~~APP BELOW~~~')

        if len(itt) == 1:
            return ""

        return itt[1]

    def full_coords(self):
        if self.coordinates_lat not in (0, None) and self.coordinates_long not in (0, None):
            return [self.coordinates_lat, self.coordinates_long]

        if (place := self.place) is not None:
            if place.coordinates_lat != 0 and place.coordinates_long != 0:
                return [place.coordinates_lat, place.coordinates_long]

        return None
    
    def close_inscriptions(self):
        chosen_items = [self]
        coords_range = 5

        chosen_items += Inscriptions.query.filter_by(place=self.place).all()

        own_coords = self.full_coords()

        if own_coords is not None:
            self_lat, self_long = own_coords
            chosen_items += Inscriptions.query.filter(
                Inscriptions.coordinates_lat >= (self_lat - coords_range),
                Inscriptions.coordinates_lat <= (self_lat + coords_range),
                Inscriptions.coordinates_long >= (self_long - coords_range),
                Inscriptions.coordinates_long <= (self_long + coords_range),
            ).all()

            close_places = Places.query.filter(
                Places.coordinates_lat >= (self_lat - coords_range),
                Places.coordinates_lat <= (self_lat + coords_range),
                Places.coordinates_long >= (self_long - coords_range),
                Places.coordinates_long <= (self_long + coords_range),
            ).all()

            for place in close_places:
                chosen_items += Inscriptions.query.filter(
                    Inscriptions.place == place
                ).all()
        
        chosen_items = set(chosen_items)

        return inscriptions_to_json(chosen_items)

    def update_str(self):
        if self.last_updated_at is None:
            return "never (either you are creating this inscription right now or this is an error)."

        if self.last_updated_by is None:
            return self.last_updated_at.strftime("%Y-%m-%d") + ", by anon"
        else:
            return self.last_updated_at.strftime("%Y-%m-%d") + ", by " + self.last_updated_by.full_name
    
    def thumbnail_url(self):
        if len(self.images) == 0:
            return None
        
        return self.images[0].image_link


class InscriptionEdited(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    inscription = db.relationship('Inscriptions', backref='revisions')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    revision_at = db.Column(db.DateTime, default=db.func.now())
    revision_comment = db.Column(db.Text)


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

    modern_state_id = db.Column(
        db.Integer, db.ForeignKey('modern_states.id'))
    modern_state = db.relationship('ModernStates', backref='places')

    pleiades_id = db.Column(db.Integer())
    geonames_id = db.Column(db.Integer())
    trismegistos_nr = db.Column(db.String(40))
    enum_lod = db.Column(db.String(150))

    def modern_state_name(self):
        if not self.modern_state:
            return '-'

        return self.modern_state.title


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


class PeopleRoles(db.Model):
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
    parent_verse_type = db.relationship('VerseTypes', remote_side=[id], backref="children")
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
    translation_author = db.Column(db.String(210))

    language = db.relationship('Languages')

    def language_title(self):
        return self.language.title

    def display(self):
        if self.translation_author:
            return self.link_to_published_translation + " (" + self.language_title() + ", " \
                + self.translation_author + ")"

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
        return self.reference_comment  # + " (" + self.zotero_item_id + ")"


class People(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))

    r1b1_link = db.Column(db.Text)
    trismegistos_link = db.Column(db.Text)
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
    people_role_id = db.Column(db.Integer, db.ForeignKey('people_roles.id'))

    gender = db.relationship('PeopleGenders', backref='people')
    age = db.relationship('PeopleAges', backref='people')
    age_expression = db.relationship('PeopleAgeExpressions', backref='people')
    age_precision = db.relationship('PeopleAgePrecision', backref='people')
    origin = db.relationship('PeopleOrigins', backref='people')
    legal_status = db.relationship('PeopleLegalStatus', backref='people')
    rank = db.relationship('PeopleRanks', backref='people')
    profession = db.relationship('PeopleProfessions', backref='people')
    role = db.relationship('PeopleRoles', backref='people')

    def display(self):
        html = Markup("<table role=\"table\">")

        def safe_title(o):
            if not o:
                return ""

            return o.title

        for col, val in [
            ("Name", self.name),
            ("Gender", safe_title(self.gender)),
            ("Age Range", safe_title(self.age) + safe_title(
                self.age_expression) + safe_title(self.age_precision)),
            ("Origin", safe_title(self.origin)),
            ("Legal Status", safe_title(self.legal_status)),
            ("Rank", safe_title(self.rank)),
            ("Profession", safe_title(self.profession)),
            ("Romans 1by1 Link", self.r1b1_link or ""),
            ("Trismegistos People-No.", self.trismegistos_link or ""),
            ("Role", safe_title(self.role)),
        ]:
            if not val:
                continue

            if col == "Age Range":
                val = safe_title(self.age)
                if self.age_expression and self.age_precision:
                    val += " [expression: " + safe_title(self.age_expression) + ", precision: " + safe_title(self.age_precision) + "]"
                elif self.age_expression:
                    val += " [expression: " + safe_title(self.age_expression) + "]"
                elif self.age_precision:
                    val += " [precision: " + safe_title(self.age_precision) + "]"

            html += Markup("<tr><th>" + col + "</th><td>")
            html += val
            html += Markup("</td></tr>")

        html += Markup("</table>")
        return html


class Religions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    enum_lod = db.Column(db.String(150))


class Images(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscriptions.id'))
    image_link = db.Column(db.Text)#
    image_alt = db.Column(db.Text)
    image_citation = db.Column(db.String(210))

    def display(self):
        img = Markup(f"<img src=\"") + self.image_link + Markup("\" alt=\"") + self.image_alt + Markup("\">")
        img_link = Markup("<a href=\"") + self.image_link + Markup("\">") + img + Markup("</a>")
        description = Markup("<p>") + self.image_alt + Markup("</p>")
        copyright = Markup("<p>") + self.image_citation + Markup("</p>")

        figure = Markup("<figure>") + img_link + Markup("<figcaption>") + description + copyright + Markup("</figcaption></figure>")

        return figure


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
                base = sorted(base, key=lambda i: getattr(
                    i, col["order"]) or VERY_LARGE_NUMBER)

            return [(getattr(i, col["render"]), linker.link(i)) for i in base]
    elif col["type"] == "reference_func":
        if hasattr(item, col["column"]):
            base = getattr(item, col["column"])

            if 'order' in col:
                base = sorted(base, key=lambda i: getattr(
                    i, col["order"]) or VERY_LARGE_NUMBER)

            return [(getattr(i, col["render"])(), linker.link(i)) for i in base]
    elif col["type"] == "custom_map":
        return (defn_parse_raw(col["column"], item), linkage)
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
        gv = sorted(gv, key=lambda x: x.title)
        out_data += [{
            "label": defn_parse_raw(grouping['representation'], gv[0]),
            "entities": gv
        }]

    out_data = sorted(out_data, key=lambda x: x['label'])

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

    elif type_['post_process'] == 'text:nl2br':
        if type(data) == list:
            return [postproc(i, type_) for i in data]

        text = data[0]

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        text = flask.Markup("<br>").join(text.split("\n"))
        return text, data[1]
    
    elif type_['post_process'] == 'allow_html':
        if type(data) == list:
            return [postproc(i, type_) for i in data]

        return flask.Markup(data[0]), data[1]

    return data


def inscriptions_to_json(inscs):
    mc = []

    for insc in inscs:
        mc += [{
            "id": insc.id,
            "long_id": insc.long_id(),
            "title": insc.title,
            "text": insc.text_only_preview(),
            "thumbnail_url": insc.thumbnail_url(),
            "item_url": flask.url_for("resource.show", name="Inscriptions", id=insc.id, _external=True),
            "coords": insc.full_coords(),
            "place": insc.place.title if insc.place else None
        }]
    
    return mc