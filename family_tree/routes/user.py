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

from family_tree import db

from family_tree.forms import (
    UpsertPersonForm
)

from family_tree.models import (
    GenderEnum,
    Person
)

from family_tree.services.user import (
    update_person
)

from family_tree.cursor import Cursor

cursor = Cursor()

bp = Blueprint('user',__name__)

@bp.before_request
def restrict_access_to_user():
    if not current_user.is_authenticated:
        app.logger.warning("Unauthorized access attempt to user routes.")
        return redirect(url_for('common.login'))
    else:
        app.logger.info(f"User {current_user.username} accessed user routes.")

@bp.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    """
    Render the user's profile page.
    """
    app.logger.info(f"Rendering profile page for user {current_user.username}.")
    form  = UpsertPersonForm()
    if request.method == 'GET' and current_user.person:
        form.first_name.data = current_user.person.first_name
        form.middle_name.data = current_user.person.middle_name
        form.last_name.data = current_user.person.last_name
        form.gender.data = current_user.person.gender.value
    if form.validate_on_submit():
        app.logger.info(f"Form submitted for user {current_user.username}.")
        if current_user.person is None:
            app.logger.info(f"Creating profile for new user {current_user.username}.")
            cursor.add(
                db, 
                Person,
                user_id=current_user.id,
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                last_name=form.last_name.data,
                gender=GenderEnum(form.gender.data)
            )
            flash('Profile created successfully!', 'success')
            app.logger.info(f"Profile created for user {current_user.username}.")
        else:
            app.logger.info(f"Updating profile for user {current_user.username}.")
            update_person(db, current_user,form)
            flash('Profile updated successfully!', 'success')
            app.logger.info(f"Profile updated for user {current_user.username}.")
    
    return render_template(
        'user/profile.html', 
        user=current_user,
        form=form)