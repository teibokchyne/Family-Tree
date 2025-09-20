from datetime import datetime
import enum

from flask_login import UserMixin

from family_tree import db, bcrypt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    person = db.relationship('Person', backref='user', uselist=False, cascade='all, delete-orphan')
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all, delete-orphan')
    important_dates = db.relationship('ImportantDates', backref='user', lazy=True, cascade='all, delete-orphan')
    contact_details = db.relationship('ContactDetails', backref='user', lazy=True, cascade='all, delete-orphan')
    def create_password_hash(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)




    # mobile_numbers = db.relationship('MobileNumber', backref='person', lazy=True, cascade='all, delete-orphan')
    # education = db.relationship('Education', backref='person', lazy=True, cascade='all, delete-orphan')
    # records = db.relationship('Record', backref='person', lazy=True, cascade='all, delete-orphan')
    # additional_info = db.relationship('AdditionalInfo', backref='person', lazy=True, cascade='all, delete-orphan', uselist=False)
    # photos = db.relationship('Photos', backref='person', lazy=True, cascade='all, delete-orphan')

class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

# Main Person entity
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name}>'

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_permanent = db.Column(db.Boolean, nullable=False)
    first_line = db.Column(db.String(255), nullable=False)
    second_line = db.Column(db.String(255))
    pin_code = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    landmark = db.Column(db.String(255))

    def __repr__(self):
        return f'<Address {self.first_line}, {self.state}, {self.country}>'

class ImportantDateTypeEnum(enum.Enum):
    BIRTH = "BIRTH"
    DEATH = "DEATH"
    MARRIAGE = "MARRIAGE"

class ImportantDates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_type = db.Column(db.Enum(ImportantDateTypeEnum), nullable=False)  # e.g., Birth, Anniversary
    date = db.Column(db.Date, nullable=False)

class ContactDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    country_code = db.Column(db.Integer)
    mobile_no = db.Column(db.String)
    email = db.Column(db.String(120))
