import pytest

from flask_login import current_user

class TestCommonRoutes:
    def test_register_sucess(self, client):
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password'
        }, follow_redirects=True)
        assert b'Registration successful' in response.data

    def test_register_failure_email(self, client, sample_user):
        # email already registered
        response = client.post('/register', data={
            'username': 'testuser2',
            'email': sample_user.email,
            'password': 'password'
        }, follow_redirects=True)
        # Check for error message or that register.html is rendered again
        assert b'Email already registered. Please log in.' in response.data  # Form is shown again

    def test_register_failure_username(self, client, sample_user):
        # email already registered
        response = client.post('/register', data={
            'username': sample_user.username,
            'email': 'test2@test.com',
            'password': 'password'
        }, follow_redirects=True)
        # Check for error message or that register.html is rendered again
        assert b'Username already registered. Please use a different one.' in response.data  # Form is shown again

    def test_login_success(self, client, authenticated_user):
        response = client.post('/login', data={
            'email': authenticated_user.email,
            'password': 'password',
            'remember': 'y'
        }, follow_redirects=True)
        assert b'Dashboard' in response.data or b'dashboard' in response.data

    def test_login_failure(self, client):
        response = client.post('/login', data={
            'email': 'test@test.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'Login Unsuccessful' in response.data

    def test_logout(self, client, sample_user):
        # First, log in
        client.post('/login', data={
            'email': sample_user.email,
            'password': 'password',
        }, follow_redirects=True)

        response = client.get('/logout', follow_redirects=True)
        print(response.data.decode())
        assert b'Welcome to Family Tree. Please log in to continue' in response.data
        assert not current_user.is_authenticated
