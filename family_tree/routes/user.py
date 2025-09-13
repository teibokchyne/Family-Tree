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

bp = Blueprint('user',__name__)

@bp.before_request
def restrict_access_to_user():
    pass