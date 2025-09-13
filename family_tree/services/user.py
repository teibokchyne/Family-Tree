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