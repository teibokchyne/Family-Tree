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
    UpsertPersonForm,
    UpsertAddressForm
)

from family_tree.models import (
    GenderEnum,
    Person,
    Address
)

from family_tree.services.user import (
    update_person,
    prefill_address_form,
    fill_address_from_form
)

from family_tree.cursor import Cursor

cursor = Cursor()

bp = Blueprint('user', __name__)


@bp.before_request
def restrict_access_to_user():
    if not current_user.is_authenticated:
        app.logger.warning("Unauthorized access attempt to user routes.")
        return redirect(url_for('common.login'))
    else:
        app.logger.info(f"User {current_user.username} accessed user routes.")


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Render the user's profile page.
    """
    app.logger.info(
        f"Rendering profile page for user {current_user.username}.")
    form = UpsertPersonForm()
    if request.method == 'GET' and current_user.person:
        form.first_name.data = current_user.person.first_name
        form.middle_name.data = current_user.person.middle_name
        form.last_name.data = current_user.person.last_name
        form.gender.data = current_user.person.gender.value
    if form.validate_on_submit():
        app.logger.info(f"Form submitted for user {current_user.username}.")
        if current_user.person is None:
            app.logger.info(
                f"Creating profile for new user {current_user.username}.")
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
            app.logger.info(
                f"Profile created for user {current_user.username}.")
        else:
            app.logger.info(
                f"Updating profile for user {current_user.username}.")
            update_person(db, current_user, form)
            flash('Profile updated successfully!', 'success')
            app.logger.info(
                f"Profile updated for user {current_user.username}.")

    return render_template(
        'user/profile.html',
        user=current_user,
        form=form)


@bp.route('/address', methods=['GET', 'POST'])
@login_required
def address():
    """
    Render and process the user's address form.
    """
    app.logger.info(
        f"Rendering address page for user {current_user.username}.")

    return render_template(
        'user/address.html',
        addresses=current_user.addresses
    )


@bp.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
    """
    Render the add address page if user has less than two addresses.
    """
    app.logger.info(
        f"Rendering add address page for user {current_user.username}.")
    if current_user.addresses and len(current_user.addresses) >= 2:
        app.logger.info(
            f"User {current_user.username} already has two addresses.")
        flash('You have already added both permanent and current addresses.', 'info')
        return redirect(url_for('user.address'))
    form = UpsertAddressForm()
    if form.validate_on_submit():
        is_permanent = form.is_permanent.data
        if current_user.addresses:
            if any(addr.is_permanent == is_permanent for addr in current_user.addresses):
                app.logger.info(
                    f"User {current_user.username} attempted to add duplicate address type.")
                flash('You have already added this type of address.', 'warning')
                return redirect(url_for('user.address'))
        cursor.add(
            db,
            Address,
            user_id=current_user.id,
            is_permanent=is_permanent,
            first_line=form.first_line.data,
            second_line=form.second_line.data,
            pin_code=form.pin_code.data,
            state=form.state.data,
            country=form.country.data,
            landmark=form.landmark.data
        )
        flash('Address added successfully!', 'success')
        app.logger.info(f"Address added for user {current_user.username}.")
        return redirect(url_for('user.address'))
    return render_template(
        'user/add_address.html',
        form=form
    )


@bp.route('/edit_address/<int:address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    """
    Render the edit address page for a specific address.
    """
    app.logger.info(
        f"Rendering edit address page for user {current_user.username}, address ID {address_id}.")
    address = cursor.query(db, Address, filter_by=True,
                           id=address_id, user_id=current_user.id).first()
    if not address:
        app.logger.warning(
            f"Address ID {address_id} not found for user {current_user.username}.")
        flash('Address not found.', 'danger')
        return redirect(url_for('user.address'))

    form = UpsertAddressForm()
    if request.method == 'GET':
        prefill_address_form(form, address)

    if form.validate_on_submit():
        if address.is_permanent != form.is_permanent.data:
            if len(current_user.addresses) >= 2:
                other_address = cursor.query(db, Address,
                                             filter_by=True, is_permanent=form.is_permanent.data,
                                             user_id=current_user.id).first()
                if other_address:
                    app.logger.info(
                        f"User {current_user.username} attempted to change to duplicate address type.")
                    app.logger.info(
                        f'The other address ID is {other_address.id}, is_permanent: {other_address.is_permanent}, has been changed to {address.is_permanent}')
                    other_address.is_permanent = address.is_permanent
                    db.session.commit()

        fill_address_from_form(address, form)

        db.session.commit()
        flash('Address updated successfully!', 'success')
        app.logger.info(
            f"Address ID {address_id} updated for user {current_user.username}.")
        return redirect(url_for('user.address'))

    return render_template(
        'user/edit_address.html',
        form=form,
        address=address
    )

@bp.route('/display_address/<int:address_id>')
@login_required
def display_address(address_id):
    """
    Render the display address page for a specific address.
    """
    app.logger.info(
        f"Rendering display address page for user {current_user.username}, address ID {address_id}.")
    address = cursor.query(db, Address, filter_by=True,
                           id=address_id, user_id=current_user.id).first()
    if not address:
        app.logger.warning(
            f"Address ID {address_id} not found for user {current_user.username}.")
        flash('Address not found.', 'danger')
        return redirect(url_for('user.address'))

    return render_template(
        'user/display_address.html',
        address=address
    )

@bp.route('/delete_address/<int:address_id>', methods=['POST'])
@login_required
def delete_address(address_id):
    """
    Render the delete address confirmation page and handle deletion.
    """
    app.logger.info(
        f"Rendering delete address page for user {current_user.username}, address ID {address_id}.")
    address = cursor.query(db, Address, filter_by=True,
                           id=address_id, user_id=current_user.id).first()
    if not address:
        app.logger.warning(
            f"Address ID {address_id} not found for user {current_user.username}.")
        flash('Address not found.', 'danger')

    if request.method == 'POST':
        cursor.delete(db, Address, id=address_id, user_id=current_user.id)
        flash('Address deleted successfully!', 'success')
        app.logger.info(
            f"Address ID {address_id} deleted for user {current_user.username}.")

    return redirect(url_for('user.address'))
