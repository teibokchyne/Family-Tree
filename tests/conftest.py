
import pytest

import family_tree

from family_tree import create_app, db
from family_tree.models import User, Person
from tests.testconfig import TestConfig

@pytest.fixture()
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def sample_user(client):
    client.post('/register', data=dict(
        username='testuser',    
        email='test@test.com',
        password='password'
        ), follow_redirects=True)
    user = User.query.filter_by(username='testuser', email='test@test.com').first()
    return user

@pytest.fixture()
def authenticated_user(sample_user, client):
    client.post('/login', data=dict(
        email = sample_user.email,
        password='password'
    ), follow_redirects=True)
    return sample_user