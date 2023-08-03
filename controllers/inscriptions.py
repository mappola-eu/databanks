from flask import Blueprint, url_for, render_template
from ..models import Inscriptions, db, get_enum
from ..models import ObjectDecorationTags, Languages, VerseTypes, DatingCriteria
from flask_security import login_required

inscriptions = Blueprint('inscriptions', __name__)


@inscriptions.route("/map")
def map():
    inscs = Inscriptions.query.all()

    mc = inscriptions_to_json(inscs)

    return render_template("inscriptions/map.html", mc=mc)


def inscriptions_to_json(inscs):
    mc = []

    for insc in inscs:
        mc += [{
            "id": insc.id,
            "long_id": insc.long_id(),
            "title": insc.title,
            "text": insc.text_only_preview(),
            "thumbnail_url": insc.thumbnail_url(),
            "item_url": url_for("resource.show", name="Inscriptions", id=insc.id, _external=True),
            "coords": insc.full_coords(),
            "place": insc.place.title if insc.place else None
        }]
    
    return mc