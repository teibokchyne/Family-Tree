import pytest

from flask_login import current_user

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
        assert b'Username already registered. Please use a different one.' in response.data  # Form is shown again

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

        assert response.status_code == 200 or response.status_code == 302  # Depending on redirect behavior
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

        assert response.status_code == 200 or response.status_code == 302  # Depending on redirect behavior
        assert b'Profile updated successfully!' in response.data