class TestUserService:
    def test_update_person(self, db, app):
        with app.app_context():
            from werkzeug.datastructures import MultiDict

            from family_tree.forms import UpsertPersonForm
            from family_tree.models import (
                User,
                Person
            )
            from family_tree.services.user import update_person
            new_user = User(id=1,
                            username='newusername',
                            email='newuseremail@email.com',
                            password_hash='password')
            db.session.add(new_user)
            db.session.commit()

            # Create a person for the user
            person = Person(
                user_id=1,
                first_name="Old",
                middle_name="Name",
                last_name="User",
                gender="MALE"
            )
            db.session.add(person)
            db.session.commit()

            # Simulate form data
            form_data = {
                'first_name': 'New',
                'middle_name': 'Mid',
                'last_name': 'User',
                'gender': 'FEMALE'
            }
            form = UpsertPersonForm(formdata=MultiDict(form_data))
            assert form.validate() 

            # Call the service
            user = User.query.filter_by(id=1).first()
            update_person(db, user, form)

            # Fetch updated person
            person_id = Person.query.filter_by(user_id=1).first().id
            updated_person = Person.query.filter_by(id=person_id).first()
            assert updated_person.first_name == 'New'
            assert updated_person.gender.value == 'FEMALE'
