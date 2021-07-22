from flask import *
from ..models import db, get_enum
from flask_security import login_required

enum = Blueprint('enum', __name__)

@login_required
@enum.route("/<name>")
def show(name):
    try:
        enum = get_enum(name)
    except: abort(403)

    return render_template("enum/show.html", name=name, enum=enum)

@login_required
@enum.route("/<name>/edit/<id>", methods=["GET", "POST"])
def edit(name, id):
    try:
        enum = get_enum(name)
    except: abort(403)

    item = enum.query.get_or_404(id)

    if request.method == "POST":
        item.title = request.form['title']
        db.session.commit()

    return render_template("enum/edit.html", name=name, enum=enum, item=item)