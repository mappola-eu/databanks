from flask import *
from ..models import Inscriptions, db, get_enum
from ..models import ObjectDecorationTags, Languages, VerseTypes, DatingCriteria
from flask_security import login_required

inscriptions = Blueprint('inscriptions', __name__)


@inscriptions.route("/map")
def map():
    inscs = Inscriptions.query.all()

    mc = []

    for insc in inscs:
        mc += [{
            "id": insc.id,
            "long_id": insc.long_id(),
            "title": insc.title,
            "text": insc.text_only_preview(),
            "thumbnail_url": None,
            "coords": insc.full_coords(),
            "place": insc.place.title if insc.place else None
        }]

    return render_template("inscriptions/map.html", mc=mc)