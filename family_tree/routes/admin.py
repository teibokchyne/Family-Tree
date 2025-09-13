from flask import (
    Blueprint, 
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app as app
    )

from flask_login import current_user, login_required

from family_tree import (
    db,
    bcrypt
)

from family_tree.models import (
    User,
    Person
)

from family_tree.cursor import Cursor

cursor = Cursor()   

bp = Blueprint('admin',__name__)

@bp.before_request
def restrict_access_to_admin():
    pass
