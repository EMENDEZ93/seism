from flask import request
#from flask.ext.wtf import Form
from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
from models import Country


class CountryForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])

class DepartmentForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])

class CityForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
