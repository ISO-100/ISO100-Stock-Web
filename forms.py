from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators
from wtforms.validators import Required, Email, EqualTo

# Define the login form (WTForms)

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Required(),
                            validators.EqualTo('confirm', message="Password must match")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and the Privacy Notice',[validators.Required()])