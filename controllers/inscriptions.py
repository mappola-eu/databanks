from flask import *
from ..models import Inscriptions, db, get_enum
from flask_security import login_required

inscriptions = Blueprint('inscriptions', __name__)

@inscriptions.route("/<id>")
def show(id):
    inscription = Inscriptions.query.get_or_404(id)
    return render_template("inscriptions/show.html", inscription=inscription)

@login_required
@inscriptions.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    inscription = Inscriptions.query.get_or_404(id)

    if request.method == "POST":
        accepted_properties = [
            "title",
            "trismegistos_nr",
            "text_interpretative_form",
            "text_diplomatic_form",
            "text_metrics_visualised_form",
            "place_id",
            "find_comment",
            "current_location_id",
            "object_type_id",
            "object_material_id",
            "object_preservation_state_id",
            "object_execution_technique_id",
            "object_decoration_comment",
            #"decoration_tags"
            "object_text_layout_comment",
            "text_function_id",
            #"languages",
            #"verse_types",
            "apparatus_criticus"
        ]

        for prop in accepted_properties:
            inscription.__setattr__(prop, request.form[prop])

        db.session.commit()

        flash('Changes committed successfully')

        return redirect(url_for('inscriptions.edit', id=inscription.id))

    return render_template("inscriptions/edit.html", inscription=inscription, get_enum=get_enum,
                           get_ids = lambda list: [i.id for i in list])