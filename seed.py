from family_tree import db

from family_tree.models import (
    User,
    Person
)

def seed_database():
    db.create_all()
