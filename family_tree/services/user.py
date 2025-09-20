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