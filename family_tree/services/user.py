from flask import (
    flash,
    current_app as app
)

from family_tree.cursor import Cursor

cursor = Cursor()

def update_person(db, user, form):
    if form.first_name.data is not None:
        user.person.first_name = form.first_name.data
    if form.middle_name.data is not None:
        user.person.middle_name = form.middle_name.data
    if form.last_name.data is not None:
        user.person.last_name = form.last_name.data
    if form.gender.data is not None:
        user.person.gender = form.gender.data
    db.session.commit()


def prefill_address_form(form, address):
    form.is_permanent.data = address.is_permanent
    form.first_line.data = address.first_line
    form.second_line.data = address.second_line
    form.pin_code.data = address.pin_code
    form.state.data = address.state
    form.country.data = address.country
    form.landmark.data = address.landmark


def fill_address_from_form(address, form):
    address.is_permanent = form.is_permanent.data
    address.first_line = form.first_line.data
    address.second_line = form.second_line.data
    address.pin_code = form.pin_code.data
    address.state = form.state.data
    address.country = form.country.data
    address.landmark = form.landmark.data


def get_relative_details(db, table, relatives):
    relative_details = []
    for rel in relatives:
        relative_user = cursor.query(
            db, table, filter_by=True, id=rel.relative_user_id).first()
        person = relative_user.person
        if person:
            relative_details.append({
                'first_name': person.first_name,
                'middle_name': person.middle_name,
                'last_name': person.last_name,
                'relationship': rel.relation_type.value,
                'relative_user_id': rel.relative_user_id
            })
    return relative_details

def prefill_upsert_relative_form(db, user_table, user_id, form):
    all_users = cursor.query(db, user_table, filter_by=False).all()
    form.relative_user_id.choices = [
        (u.id, f'{u.person.first_name} {u.person.last_name}')
        for u in all_users 
        if u.id != user_id and u.person is not None 
        ]

def check_relative_constraints(db, user_table, relatives_table, user, form):
    # Check if the relative exists
    relative_user = cursor.query(
        db, user_table, filter_by=True, id=int(form.relative_user_id.data)).first()
    if not relative_user:
        app.logger.warning("Relative user not found.")
        flash("The selected relative does not exist.", "danger")
        return False

    # Check if the user is trying to add themselves as a relative
    if relative_user and relative_user.id == user.id:
        app.logger.warning("User attempted to add themselves as a relative.")
        flash("You cannot add yourself as a relative.", "danger")
        return False

    # Check for duplicate relationships. There can only be one relationship between two users in one direction.
    existing_relation = cursor.query(
        db,
        relatives_table,
        filter_by=True,
        user_id=user.id,
        relative_user_id=int(form.relative_user_id.data)).first()
    if existing_relation:
        app.logger.warning("User attempted to add more than one relationship to a relative.")
        flash("This relationship already exists.", "danger")
        return False

    # Check that both user profiles exist
    if not user.person or not relative_user.person:
        app.logger.warning(
            "One or both of the users does not have a complete profile.")
        flash(
            "Both users must have complete profiles to establish a relationship.", "danger")
        return False

    return True

def add_relative_to_database(db, relative_table, relative_enum, user, form):
    cursor.add(
        db,
        relative_table,
        user_id=user.id,
        relative_user_id=int(form.relative_user_id.data),
        relation_type=relative_enum(form.relation_type.data)
    )
    cursor.add(
        db,
        relative_table,
        user_id=int(form.relative_user_id.data),
        relative_user_id=user.id,
        relation_type=relative_enum(
           relative_table.get_reverse_relation(form.relation_type.data)
           )
    )
    app.logger.info(f"Relative added for user {user.username}.")


def delete_relative_from_database(db, user_table, relatives_table, user, relative_user_id):
    app.logger.info(f'Attempt to delete relative {relative_user_id} of user {user.id}')
    relation = cursor.query(db, relatives_table, filter_by=True, user_id=user.id, relative_user_id=relative_user_id).first()
    if not relation:
        app.logger.info(f'Could not find relative of user {user.id} with relative user id {relative_user_id}')
        flash(f'Could not find relation with relative user id {relative_user_id}')
        return False 
    else:
        reverse_relation = cursor.query(db, relatives_table, filter_by=True, user_id=relative_user_id, relative_user_id=user.id).first()
        if not reverse_relation:
            app.logger.info(f'Could not find reverse relation from relative {relative_user_id} to user {user.id}')
        else:
            cursor.delete(db, relatives_table, user_id=relative_user_id, relative_user_id=user.id)
            app.logger.info(f'Successfully deleled reverse relation from relative {relative_user_id} to user {user.id}')
        cursor.delete(db, relatives_table, user_id=user.id, relative_user_id=relative_user_id)
        app.logger.info(f'Successfully deleled relation from user {user.id} to relative {relative_user_id}')
        return True
            