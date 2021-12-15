from flask import *
from ..models import db, get_enum, defn, get_defn, defn_parse, render_column, defn_parse_raw
from flask_security import login_required

resource = Blueprint('resource', __name__)

@resource.route("/<name>")
def index(name):
    try:
        R = get_enum(name)
    except: abort(403)

    return render_template("resource/index.html", name=name, R=R, defn=get_defn(name, scope="summary"),
    defn_parse=defn_parse)

@resource.route("/<name>/show/<id>", methods=["GET", "POST"])
def show(name, id):
    try:
        R = get_enum(name)
    except: abort(403)

    item = R.query.get_or_404(id)

    return render_template("resource/show.html", name=name, R=R, item=item,
    defn=get_defn(name, scope="display"), defn_parse=defn_parse, render_column=render_column,
    defn_parse_raw=defn_parse_raw)

@login_required
@resource.route("/<name>/edit/<id>", methods=["GET", "POST"])
def edit(name, id):
    try:
        R = get_enum(name)
    except: abort(403)

    item = R.query.get_or_404(id)

    if request.method == "POST":
        item.title = request.form['title']
        db.session.commit()

    return render_template("resource/edit.html", name=name, R=R, item=item,
    defn=get_defn(name, scope="display"), defn_parse=defn_parse, render_column=render_column,
    defn_parse_raw=defn_parse_raw)

@login_required
@resource.route("/<name>/delete/<id>", methods=["GET", "POST"])
def delete(name, id):
    try:
        enum = get_enum(name)
    except: abort(403)

    item = enum.query.get_or_404(id)

    if request.method == "POST":
        item.title = request.form['title']
        db.session.commit()

    return render_template("enum/edit.html", name=name, enum=enum, item=item)

@login_required
@resource.route("/<name>/new", methods=["GET", "POST"])
def new(name):
    try:
        enum = get_enum(name)
    except: abort(403)

    item = enum()
    item.title = ""

    if request.method == "POST":
        item.title = request.form['title']
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('enum.show', name=name))

    return render_template("enum/new.html", name=name, enum=enum, item=item)