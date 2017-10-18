from flask import request
#from flask.ext.wtf import Form
from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired

from wtforms import Form, BooleanField, StringField, PasswordField, validators
from models import Country


class CountryForm(Form):
    name = StringField('Username', [validators.Length(min=4, max=25)])
