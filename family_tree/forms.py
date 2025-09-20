from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField, 
    EmailField,
    BooleanField,
    SelectField
    )
from wtforms.validators import (
    DataRequired, 
    Email,
    Optional
)

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class UpsertPersonForm(FlaskForm):
    gender = SelectField('Gender', choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other')
    ], validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Add/Edit Person')

class UpsertAddressForm(FlaskForm):
    is_permanent = BooleanField('Permanent Address')
    first_line = StringField('Address Line 1', validators=[DataRequired()])
    second_line = StringField('Address Line 2')
    pin_code = StringField('Pin Code', validators=[DataRequired()])
    state = StringField('State', default='Meghalaya', validators=[DataRequired()])
    country = StringField('Country', default='India', validators=[DataRequired()])
    landmark = StringField('Landmark')
    submit = SubmitField('Submit')
