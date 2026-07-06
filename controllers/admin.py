from flask import *
from flask_security import login_required, current_user
from ..models import db

admin = Blueprint('admin', __name__)

@admin.route("/")
@login_required
def index():
    if not current_user.has_admin_permissions():
        abort(404)

    return render_template("admin/index.html")