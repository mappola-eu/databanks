from flask import *
from ..models import Inscriptions

inscriptions = Blueprint('inscriptions', __name__)

@inscriptions.route("/<id>")
def show(id):
    inscription = Inscriptions.query.get_or_404(id)
    return render_template("inscriptions/show.html", inscription=inscription)