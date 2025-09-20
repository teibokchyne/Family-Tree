import pytest

from flask_login import current_user

from family_tree.models import (
    User
)


class TestCommonRoutes:
    def test_register_sucess(self, client):
        response = client.post('/register', data={
            'username': 'sampleuser',
            'email': 'sampleuser@example.com',
            'password': 'pass'
        }, follow_redirects=True)
        assert b'Registration successful' in response.data

    def test_register_failure_email(self, client):
        # register a user first
        response = client.post('/register', data={
            'username': 'sampleuser',
            'email': 'sampleuser@example.com',
            'password': 'pass'
        }, follow_redirects=True)

        # email already registered
        response = client.post('/register', data={
            'username': 'sampleuser2',
            'email': 'sampleuser@example.com',
            'password': 'pass'
        }, follow_redirects=True)
        # Check for error message or that register.html is rendered again
        assert b'Email already registered. Please log in.' in response.data  # Form is shown again

    def test_register_failure_username(self, client):
        # register a user first
        response = client.post('/register', data={
            'username': 'sampleuser',
            'email': 'sampleuser@example.com',
            'password': 'pass'
        }, follow_redirects=True)

        # email already registered
        response = client.post('/register', data={
            'username': 'sampleuser',
            'email': 'sampleuser2@example.com',
            'password': 'pass'
        }, follow_redirects=True)
        # Check for error message or that register.html is rendered again
        # Form is shown again
        assert b'Username already registered. Please use a different one.' in response.data

    def test_login_success(self, client, registered_user):
        response = client.post('/login', data={
            'email': registered_user.email,
            'password': 'pass',
            'remember': 'y'
        }, follow_redirects=True)
        assert b'Dashboard' in response.data or b'dashboard' in response.data

    def test_login_failure(self, client):
        response = client.post('/login', data={
            'email': 'test@test.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'Login Unsuccessful' in response.data

    def test_logout(self, client, registered_user):
        # First, log in
        client.post('/login', data={
            'email': registered_user.email,
            'password': 'pass',
            'remember': 'y'
        })

        response = client.get('/logout', follow_redirects=True)
        print(response.data.decode())
        assert b'Welcome to Family Tree. Please log in to continue' in response.data
        assert not current_user.is_authenticated


class TestUserRoutes:
    def test_profile_creation(self, client):
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        response = client.post('/profile', data={
            'first_name': 'John',
            'middle_name': 'M',
            'last_name': 'Doe',
            'gender': 'MALE'
        })

        # Depending on redirect behavior
        assert response.status_code == 200 or response.status_code == 302
        assert b'Profile created successfully!' in response.data

    def test_profile_update(self, client):
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Create initial profile
        client.post('/profile', data={
            'first_name': 'John',
            'middle_name': 'M',
            'last_name': 'Doe',
            'gender': 'MALE'
        })

        response = client.post('/profile', data={
            'first_name': 'Jane',
            'middle_name': 'A',
            'last_name': 'Smith',
            'gender': 'FEMALE'
        })

        # Depending on redirect behavior
        assert response.status_code == 200 or response.status_code == 302
        assert b'Profile updated successfully!' in response.data

    def test_address(self, client):
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Now, access the address page
        response = client.get('/address')
        assert response.status_code == 200
        assert b'Your Addresses' in response.data or b'No Addresses Found' in response.data

    def test_add_address_success(self, client):
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)
        # Now, add an address
        response = client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)
        assert response.status_code == 200 or response.status_code == 302
        assert b'Address added successfully!' in response.data

    def test_add_address_success(self, client):
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)
        # Now, add an address
        response = client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)
        assert response.status_code == 200 or response.status_code == 302
        assert b'Address added successfully!' in response.data

    def test_add_address_failure_1(self, client):
        # Failure when trying to add more than two addresses
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Now, add an address
        response = client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)

        # Now, add a second address
        response = client.post('/add_address', data={
            'is_permanent': '',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)

        # Now try to add a third address using GET
        response = client.get('/add_address', follow_redirects=True)

        # Now, add a third address using POST
        response_2 = client.post('/add_address', data={
            'is_permanent': '',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)

        assert response.status_code == 200 or response.status_code == 302
        assert b'You have already added both permanent and current addresses.' in response.data
        assert response_2.status_code == 200 or response_2.status_code == 302
        assert b'You have already added both permanent and current addresses.' in response_2.data

    def test_add_address_failure_2(self, client):
        # Failure when trying to add address of a permanent type that already exists
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Now, add an address
        client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)

        # Now try to add a permanent address
        response = client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '456 Another St',
            'second_line': 'Apt 5C',
            'pin_code': '67890',
            'state': 'Another State',
            'country': 'Another Country',
            'landmark': 'Near Mall'
        }, follow_redirects=True)

        assert response.status_code == 200 or response.status_code == 302
        assert b'You have already added this type of address.' in response.data

    def test_add_address_failure_3(self, client):
        # Failure when trying to add address of a current type that already exists
        client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'pass'
        })
        # First, log in
        client.post('/login', data={
            'email': 'newuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Now, add an address
        client.post('/add_address', data={
            'is_permanent': '',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)

        # Now try to add a permanent address
        response = client.post('/add_address', data={
            'is_permanent': '',
            'first_line': '456 Another St',
            'second_line': 'Apt 5C',
            'pin_code': '67890',
            'state': 'Another State',
            'country': 'Another Country',
            'landmark': 'Near Mall'
        }, follow_redirects=True)

        assert response.status_code == 200 or response.status_code == 302
        assert b'You have already added this type of address.' in response.data

    def test_edit_address_success(self, client):
        client.post('/register', data={
            'username': 'edituser',
            'email': 'edituser@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'edituser@example.com',
            'password': 'pass',
        }, follow_redirects=True)
        # Add a permanent address
        client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': 'Old Line',
            'second_line': 'Old Second',
            'pin_code': '11111',
            'state': 'OldState',
            'country': 'OldCountry',
            'landmark': 'Old Landmark'
        }, follow_redirects=True)
        # Get address id
        from family_tree.models import User
        user = User.query.filter_by(email='edituser@example.com').first()
        address_id = user.addresses[0].id
        # Edit the address
        response = client.post(f'/edit_address/{address_id}', data={
            'is_permanent': 'y',
            'first_line': 'New Line',
            'second_line': 'New Second',
            'pin_code': '22222',
            'state': 'NewState',
            'country': 'NewCountry',
            'landmark': 'New Landmark'
        }, follow_redirects=True)
        assert b'Address updated successfully!' in response.data
        assert b'New Line' in response.data

    def test_edit_address_duplicate_type(self, client):
        from family_tree.models import Address

        client.post('/register', data={
            'username': 'edituser2',
            'email': 'edituser2@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'edituser2@example.com',
            'password': 'pass',
        }, follow_redirects=True)
        # Add permanent and current addresses
        client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': 'Perm',
            'second_line': '',
            'pin_code': '11111',
            'state': 'State',
            'country': 'Country',
            'landmark': ''
        }, follow_redirects=True)
        client.post('/add_address', data={
            'is_permanent': '',
            'first_line': 'Curr',
            'second_line': '',
            'pin_code': '22222',
            'state': 'State',
            'country': 'Country',
            'landmark': ''
        }, follow_redirects=True)
        from family_tree.models import User
        user = User.query.filter_by(email='edituser2@example.com').first()
        perm_address_id = [a.id for a in user.addresses if a.is_permanent][0]
        curr_address_id = [
            a.id for a in user.addresses if not a.is_permanent][0]

        response = client.post(f'/edit_address/{curr_address_id}', data={
            'is_permanent': 'y',
            'first_line': 'Curr',
            'second_line': '',
            'pin_code': '22222',
            'state': 'State',
            'country': 'Country',
            'landmark': ''
        }, follow_redirects=True)

        # Current address should change type to permanent
        curr_address = Address.query.filter_by(id=curr_address_id).first()
        assert curr_address.is_permanent == True

        # Permanent address should change type to current
        perm_address = Address.query.filter_by(id=perm_address_id).first()
        assert perm_address.is_permanent == False

    def test_edit_address_not_found(self, client):
        client.post('/register', data={
            'username': 'edituser3',
            'email': 'edituser3@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'edituser3@example.com',
            'password': 'pass',
        }, follow_redirects=True)
        # Try to edit a non-existent address
        response = client.post('/edit_address/9999', data={
            'is_permanent': 'y',
            'first_line': 'Does Not Exist',
            'second_line': '',
            'pin_code': '00000',
            'state': 'None',
            'country': 'None',
            'landmark': ''
        }, follow_redirects=True)
        assert b'Address not found.' in response.data

    def test_display_address_success(self, client):
        # Register and log in
        client.post('/register', data={
            'username': 'displayuser',
            'email': 'displayuser@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'displayuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Add an address
        client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '123 Main St',
            'second_line': 'Apt 4B',
            'pin_code': '12345',
            'state': 'State',
            'country': 'Country',
            'landmark': 'Near Park'
        }, follow_redirects=True)

        # Get the address id
        from family_tree.models import User
        user = User.query.filter_by(email='displayuser@example.com').first()
        address_id = user.addresses[0].id

        # Display the address
        response = client.get(f'/display_address/{address_id}')
        assert response.status_code == 200
        assert b'Delete Address' in response.data
        assert b'123 Main St' in response.data

    def test_display_address_not_found(self, client):
        # Register and log in
        client.post('/register', data={
            'username': 'displayuser2',
            'email': 'displayuser2@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'displayuser2@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Try to display a non-existent address
        response = client.get('/display_address/9999', follow_redirects=True)
        assert b'Address not found.' in response.data or b'No Addresses Found' in response.data

    def test_delete_address_success(self, client):
        # Register and log in
        client.post('/register', data={
            'username': 'deleteuser',
            'email': 'deleteuser@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'deleteuser@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Add an address
        client.post('/add_address', data={
            'is_permanent': 'y',
            'first_line': '456 Delete St',
            'second_line': 'Apt 9C',
            'pin_code': '54321',
            'state': 'DeleteState',
            'country': 'DeleteCountry',
            'landmark': 'Delete Landmark'
        }, follow_redirects=True)

        # Get the address id
        from family_tree.models import User
        user = User.query.filter_by(email='deleteuser@example.com').first()
        address_id = user.addresses[0].id

        # Delete the address
        response = client.post(
            f'/delete_address/{address_id}', follow_redirects=True)
        assert response.status_code == 200 or response.status_code == 302
        assert b'Address deleted successfully!' in response.data

        # Confirm address is gone
        user = User.query.filter_by(email='deleteuser@example.com').first()
        assert not user.addresses

    def test_delete_address_not_found(self, client):
        # Register and log in
        client.post('/register', data={
            'username': 'deleteuser2',
            'email': 'deleteuser2@example.com',
            'password': 'pass'
        })
        client.post('/login', data={
            'email': 'deleteuser2@example.com',
            'password': 'pass',
        }, follow_redirects=True)

        # Try to delete a non-existent address
        response = client.post('/delete_address/9999', follow_redirects=True)
        assert b'Address not found.' in response.data or b'No Addresses Found' in response.data
