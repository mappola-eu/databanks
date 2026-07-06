from flask import *
from flask_security import login_required, current_user, hash_password
from ..models import db, User, Role, Inscriptions

admin = Blueprint('admin', __name__)

@admin.route("/")
@login_required
def index():
    if not current_user.has_admin_permissions():
        abort(404)

    return render_template("admin/index.html")



@admin.route("/inscription-reassign", methods=["GET", "POST"])
@login_required
def inscription_reassign():
    if not current_user.has_admin_permissions():
        abort(404)

    ok = False

    if request.method == "POST":
        inscription = Inscriptions.query.get_or_404(request.form['inscription'])
        user = User.query.get_or_404(request.form['user'])

        inscription.last_updated_by = user
        db.session.commit()

        ok = True

    users = User.query.all()
    return render_template("admin/inscription_reassign.html", users=users, ok=ok)


# ########################################################
# User management
# ########################################################

@admin.route("/user")
@login_required
def user():
    if not current_user.has_admin_permissions():
        abort(404)

    users = User.query
    return render_template("admin/user/index.html", users=users)


@admin.route("/user/<u>", methods=["GET", "POST"])
@login_required
def edit_user(u):
    if not current_user.has_admin_permissions():
        abort(404)

    user = User.query.get_or_404(u)
    roles = Role.query.all()

    if request.method == "POST":
        user.full_name = request.form['full_name']
        user.active = 'active' in request.form

        if request.form['password']:
            user.password = hash_password(request.form['password'])

        for role in roles:
            if str(role.id) in request.form.getlist('roles'):
                if role not in user.roles:
                    user.roles.append(role)
            else:
                if role in user.roles:
                    user.roles.remove(role)
    
        db.session.commit()

    return render_template("admin/user/edit.html", user=user, existing=True, roles=roles)


@admin.route("/user/new", methods=["GET", "POST"])
@login_required
def new_user():
    if not current_user.has_admin_permissions():
        abort(404)

    user = User(email="", full_name="")
    roles = Role.query.all()

    if request.method == "POST":
        user = current_app.security.datastore.create_user(email=request.form['email'])
        user.full_name = request.form['full_name']
        user.active = 'active' in request.form
        user.password = hash_password(request.form['password'])

        for role in roles:
            if str(role.id) in request.form.getlist('roles'):
                if role not in user.roles:
                    user.roles.append(role)
            else:
                if role in user.roles:
                    user.roles.remove(role)
    
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.edit_user', u=user.id))

    return render_template("admin/user/new.html", user=user, existing=False, roles=roles)