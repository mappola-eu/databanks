from flask import *
from ..models import db, get_enum, defn, get_defn, defn_parse, render_column, defn_parse_raw, defn_snippet
from flask_security import login_required

resource = Blueprint('resource', __name__)


@resource.context_processor
def inject_resource_helpers():
    return {
        "defn_parse": defn_parse,
        "render_column": render_column,
        "defn_parse_raw": defn_parse_raw,
        "defn_snippet": defn_snippet
    }


@resource.route("/<name>")
def index(name):
    try:
        R = get_enum(name)
    except:
        abort(403)

    return render_template("resource/index.html", name=name, R=R, defn=get_defn(name, scope="summary"))


@resource.route("/<name>/show/<id>", methods=["GET", "POST"])
def show(name, id):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R.query.get_or_404(id)

    return render_template("resource/show.html", name=name, R=R, item=item, defn=get_defn(name, scope="display"))


@login_required
@resource.route("/<name>/edit/<id>", methods=["GET", "POST"])
def edit(name, id):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R.query.get_or_404(id)
    defn = get_defn(name, scope="display")

    if request.method == "POST":
        for slide in defn['slides']:
            for part in slide['parts']:
                if part["component"] == "standalone":
                    cols = [part['single']]
                elif part["component"] == "table":
                    cols = part['columns']
                else:
                    continue # for now

                for column in cols:
                    if column['type'] in ['input', 'text', 'reference', 'reference_list']:
                        # These are the simple (singular) column types
                        if column['column'] not in request.form.keys():
                            continue

                        if column['type'] in ['input', 'text']:
                            setattr(item, column['column'], request.form[column['column']])
                        elif column['type'] == 'reference':
                            cls = get_enum(column['refersto'])
                            obj = cls.query.get(request.form[column['column']])
                            setattr(item, column['column'], obj)
                        elif column['type'] == 'reference_list':
                            cls = get_enum(column['refersto'])
                            data = [cls.query.get(i) for i in request.form.getlist(column['column'])]
                            setattr(item, column['column'], data)
                    elif column['type'] in ['dimension']:
                        # Special Dimension type
                        for colname in column['column']:
                            value = request.form[colname].strip()
                            if value == '':
                                value = None
                            setattr(item, colname, value)
                    else:
                        print("LOG: unsaveable column %s" % column['column'])

        db.session.commit()
        flash('Changes committed successfully')
        return redirect(url_for('resource.edit', name=name, id=item.id))

    return render_template("resource/edit.html", name=name, R=R, item=item,
                           defn=defn, defn_parse=defn_parse, render_column=render_column,
                           defn_parse_raw=defn_parse_raw, get_enum=get_enum)


@login_required
@resource.route("/<name>/delete/<id>", methods=["GET", "POST"])
def delete(name, id):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = enum.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()

    return render_template("resource/delete.html", name=name, R=R, item=item, defn=get_defn(name, scope="display"))


@login_required
@resource.route("/<name>/new", methods=["GET", "POST"])
def new(name):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R()
    defn = get_defn(name, scope="display")
    item.title = ""

    if request.method == "POST":
        pass

        return redirect(url_for('resource.index', name=name))

    return render_template("resource/new.html", name=name, R=R, item=item,
                           defn=defn, defn_parse=defn_parse, render_column=render_column,
                           defn_parse_raw=defn_parse_raw, get_enum=get_enum)
