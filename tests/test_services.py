from family_tree import db, bcrypt

from family_tree.models import (
    User,
    GenderEnum,
    Person,
    RelativesTypeEnum,
    Relatives
)

from family_tree.forms import (
    UpsertRelativeForm
)

from family_tree.services.user import (
    check_relative_constraints,
    add_relative_to_database
)

class TestUserService:
    def create_users(self):
# 1. Create users
        users = [
            User(
                username="alice",
                email="alice@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                is_admin=True
            ),
            User(
                username="bob",
                email="bob@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                is_admin=False
            ),
            User(
                username="charlie",
                email="charlie@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                is_admin=False
            )
        ]

        db.session.bulk_save_objects(users)
        db.session.commit()

    def create_persons(self):
        # Make sure to call this function only if the following users exist already
        # Fetch user IDs 
        alice = User.query.filter_by(username="alice").first()
        bob = User.query.filter_by(username="bob").first()
        charlie = User.query.filter_by(username="charlie").first()

        # 3. Create persons
        persons = [
            Person(
                user_id=alice.id,
                gender=GenderEnum.FEMALE,
                first_name="Alice",
                middle_name="Marie",
                last_name="Anderson"
            ),
            Person(
                user_id=bob.id,
                gender=GenderEnum.MALE,
                first_name="Bob",
                middle_name=None,
                last_name="Brown"
            ),
            Person(
                user_id=charlie.id,
                gender=GenderEnum.OTHER,
                first_name="Charlie",
                middle_name="Lee",
                last_name="Campbell"
            )
        ]

        db.session.bulk_save_objects(persons)
        db.session.commit()

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

    def test_check_relative_constraints(self, db):
        from werkzeug.datastructures import MultiDict

        self.create_users()

        self.create_persons()

        # TEST 1: TEST TO SEE IF RELATION WITH NON-EXISTENT RELATIVE IS FORMED
        form_data = {
            'relative_user_id': 9999,
            'relation_type': 'PARENT'
        }
        alice = User.query.filter_by(id=1).first()
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice, form)
        assert result == False

        # TEST 2: TEST TO SEE IF RELATION WITH SELF IS FORMED
        form_data = {
            'relative_user_id': 1,
            'relation_type': 'PARENT'
        }
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice, form)
        assert result == False

        # TEST 3: TEST TO SEE IF A SECOND RELATIONSHIP IS ALLOWED
        rel1 = Relatives(user_id=1, relative_user_id=2, relation_type='PARENT')
        rel2 = Relatives(user_id=2, relative_user_id=1, relation_type='CHILD')
        db.session.add(rel1)
        db.session.add(rel2)
        db.session.commit()

        form_data = {
            'relative_user_id': 2,
            'relation_type': 'SIBLING'
        }
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice, form)
        assert result == False

        # TEST 4: TEST TO SEE IF A RELATION IS ADDED WITHOUT PROFILE
        # 1. Create users
        users2 = [
            User(
                username="alice2",
                email="alice2@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                is_admin=True
            ),
            User(
                username="bob2",
                email="bob2@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                is_admin=False
            ),
            User(
                username="charlie2",
                email="charli2e@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                is_admin=False
            )
        ]

        db.session.bulk_save_objects(users2)
        db.session.commit()

        # ALICE HAS PROFILE, ALICE2 DOES NOT
        form_data = {
            'relative_user_id': 4,
            'relation_type': 'SIBLING'
        }
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice, form)
        assert result == False

        # ALICE2 HAS NO PROFILE, ALICE DOES 
        form_data = {
            'relative_user_id': 1,
            'relation_type': 'SIBLING'
        }
        alice2 = User.query.filter_by(id=4).first()
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice2, form)
        assert result == False

        # NEITHER ALICE2 NOR BOB2 HAVE PROFILES
        form_data = {
            'relative_user_id': 5,
            'relation_type': 'SIBLING'
        }
        alice2 = User.query.filter_by(id=4).first()
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice2, form)
        assert result == False

        # TEST IF RETURN VALID IF ALL CONDITIONS ARE MET
        form_data = {
            'relative_user_id': 3,
            'relation_type': 'SIBLING'
        }
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        result = check_relative_constraints(db, User, Relatives, alice, form)
        assert result == True

    def test_add_relative_to_database(self, db):
        from werkzeug.datastructures import MultiDict

        self.create_users()
        self.create_persons()

        form_data = {
            'relative_user_id' : 2,
            'relation_type' : 'PARENT'
        }
        alice = User.query.filter_by(id=1).first()
        form = UpsertRelativeForm(formdata=MultiDict(form_data))
        add_relative_to_database(db, Relatives, RelativesTypeEnum, alice, form)

        rel1 = Relatives.query.filter_by(user_id=1).first()
        rel2 = Relatives.query.filter_by(user_id=2).first()
        rel_count = len(Relatives.query.all())
        
        assert rel1 is not None
        assert rel2 is not None 
        assert rel_count == 2
        assert rel1.relation_type.value == 'PARENT'
        assert rel2.relation_type.value == 'CHILD'