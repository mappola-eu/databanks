from flask import *
from ..models import db, get_enum, defn, get_defn, defn_parse, render_column, defn_parse_raw, defn_snippet, get_rel, get_rel_defn, get_enum_with_grouping, postproc
from flask_security import login_required, current_user

from ..linkage.epidoc import full_parse_on_inscription

resource = Blueprint('resource', __name__)


@resource.context_processor
def inject_resource_helpers():
    return {
        "defn_parse": defn_parse,
        "render_column": render_column,
        "defn_parse_raw": defn_parse_raw,
        "defn_snippet": defn_snippet,
        "get_enum_with_grouping": get_enum_with_grouping,
        "postproc": postproc
    }


@resource.route("/<name>")
def index(name):
    try:
        R = get_enum(name)
    except:
        abort(403)

    return render_template("resource/index.html",
                           name=name,
                           R=R,
                           defn=get_defn(name, scope="summary"))


@resource.route("/<name>/show/<id>", methods=["GET", "POST"])
def show(name, id):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R.query.get_or_404(id)

    return render_template("resource/show.html",
                           name=name,
                           R=R,
                           item=item,
                           defn=get_defn(name, scope="display"))


@resource.route("/<name>/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(name, id):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R.query.get_or_404(id)
    defn = get_defn(name, scope="display")

    if request.method == "POST":
        item = apply_defn_post_data_to_obj(defn, item)

        db.session.commit()
        flash('Changes committed successfully.')
        return redirect(url_for('resource.edit', name=name, id=item.id))

    return render_template("resource/edit.html",
                           name=name,
                           R=R,
                           item=item,
                           defn=defn,
                           defn_parse=defn_parse,
                           render_column=render_column,
                           defn_parse_raw=defn_parse_raw,
                           get_enum=get_enum)


@resource.route("/<name>/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(name, id):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()

    return render_template("resource/delete.html",
                           name=name,
                           R=R,
                           item=item,
                           defn=get_defn(name, scope="display"))


@resource.route("/<name>/new", methods=["GET", "POST"])
@login_required
def new(name):
    try:
        R = get_enum(name)
    except:
        abort(403)

    item = R()
    defn = get_defn(name, scope="display")
    item.title = ""

    if request.method == "POST":
        item = apply_defn_post_data_to_obj(defn, item)
        db.session.add(item)
        db.session.commit()

        flash('Entity successfully created.')
        return redirect(url_for('resource.index', name=name))

    return render_template("resource/new.html",
                           name=name,
                           R=R,
                           item=item,
                           defn=defn,
                           defn_parse=defn_parse,
                           render_column=render_column,
                           defn_parse_raw=defn_parse_raw,
                           get_enum=get_enum)


@resource.route("/<name>/-/<id>/rel/<relname>")
def relindex(name, id, relname):
    try:
        R = get_enum(name)
        rel = get_rel(relname)
    except:
        abort(403)

    item = R.query.get_or_404(id)
    q = {get_rel_defn(relname)["per"]: item.id}
    relvals = rel.query.filter_by(**q).all()

    return render_template("resource/rel/index.html",
                           name=name,
                           R=R,
                           relname=relname,
                           rel=rel,
                           relvals=relvals,
                           rel_defn=get_defn(relname, scope="summary"),
                           item=item,
                           defn=get_defn(name, scope="display"))


@resource.route("/<name>/-/<id>/rel/<relname>/new", methods=["GET", "POST"])
@login_required
def relnew(name, id, relname):
    try:
        R = get_enum(name)
        rel = get_rel(relname)
    except:
        abort(403)

    rel_defn = get_defn(relname, scope="display")
    item = R.query.get_or_404(id)
    q = {get_rel_defn(relname)["per"]: item.id}
    relval = rel(**q)

    if request.method == "POST":
        relval = apply_defn_post_data_to_obj(rel_defn, relval)
        print(relval)
        db.session.add(relval)
        db.session.commit()

        flash('Relation successfully created.')
        return redirect(url_for('resource.relindex', name=name, id=id, relname=relname))

    return render_template("resource/rel/new.html",
                           name=name,
                           R=R,
                           relname=relname,
                           rel=rel,
                           relval=relval,
                           rel_defn=rel_defn,
                           item=item,
                           defn=get_defn(name, scope="display"),
                           defn_parse=defn_parse,
                           render_column=render_column,
                           defn_parse_raw=defn_parse_raw,
                           get_enum=get_enum,
                           get_rel_defn=get_rel_defn)


@resource.route("/<name>/-/<id>/rel/<relname>/show/<relid>", methods=["GET", "POST"])
def relshow(name, id, relname):
    pass


@resource.route("/<name>/-/<id>/rel/<relname>/edit/<relid>", methods=["GET", "POST"])
@login_required
def reledit(name, id, relname, relid):
    try:
        R = get_enum(name)
        rel = get_rel(relname)
    except:
        abort(403)

    rel_defn = get_defn(relname, scope="display")
    item = R.query.get_or_404(id)
    q = {get_rel_defn(relname)["per"]: item.id}
    relval = rel.query.get_or_404(relid)

    if request.method == "POST":
        relval = apply_defn_post_data_to_obj(rel_defn, relval)
        db.session.commit()
        flash('Changes committed successfully.')
        return redirect(url_for('resource.reledit', name=name, id=item.id, relname=relname, relid=relval.id))

    return render_template("resource/rel/edit.html",
                           name=name,
                           R=R,
                           relname=relname,
                           rel=rel,
                           relval=relval,
                           rel_defn=rel_defn,
                           item=item,
                           defn=get_defn(name, scope="display"),
                           defn_parse=defn_parse,
                           render_column=render_column,
                           defn_parse_raw=defn_parse_raw,
                           get_enum=get_enum,
                           get_rel_defn=get_rel_defn)


@resource.route("/<name>/-/<id>/rel/<relname>/delete/<relid>", methods=["GET", "POST"])
@login_required
def reldelete(name, id, relname, relid):
    pass

def apply_defn_post_data_to_obj(defn, obj):
    for slide in defn['slides']:
        for part in slide['parts']:
            if part["component"] == "standalone":
                cols = [part['single']]
            elif part["component"] == "table":
                cols = part['columns']
            elif part["component"] == "text_view":
                cols = [{
                    'column': part['columns']['epidoc'],
                    'type': 'text'
                }]
            else:
                continue  # for now

            for column in cols:
                #print(column)
                if column['type'] in ['input', 'text', 'numeric_input', 'boolean_input', 'reference', 'reference_list']:
                    # These are the simple (singular) column types
                    if column['column'] not in request.form.keys() and column['type'] != 'boolean_input':
                        print('xyz')
                        continue

                    if column['type'] in ['input', 'text', 'numeric_input']:
                        setattr(obj, column['column'],
                                request.form[column['column']])
                    elif column['type'] == 'boolean_input':
                        setattr(obj, column['column'],
                                column['column'] in request.form.keys())
                    elif column['type'] == 'reference':
                        cls = get_enum(column['refersto'])
                        other = cls.query.get(request.form[column['column']])
                        if 'refopt' in column.keys() and column['refopt'] and other is None:
                            setattr(obj, column['column'] + "_id", None)
                        else:
                            setattr(obj, column['column'], other)
                    elif column['type'] == 'reference_list':
                        cls = get_enum(column['refersto'])
                        data = [cls.query.get(
                            i) for i in request.form.getlist(column['column'])]
                        setattr(obj, column['column'], data)
                elif column['type'] in ['dimension']:
                    # Special Dimension type
                    for colname in column['column']:
                        value = request.form[colname].strip()
                        if value == '':
                            value = None
                        setattr(obj, colname, value)
                else:
                    print("LOG: unsaveable column %s" % column['column'])
    
    if 'add_update_user_to' in defn.keys():
        setattr(obj, defn['add_update_user_to'], current_user)

    if 'perform_epidoc_update' in defn.keys():
        obj = full_parse_on_inscription(obj)

    return obj