# -*- coding: utf-8 -*-
from flask import request
#from flask.ext.wtf import Form
from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, DateField, TextField, SelectField, DecimalField, DateTimeField
from models import Country, City


class CountryForm(Form):
    name = StringField('Pais', [validators.Length(min=4, max=25)])


class DepartmentForm(Form):
    name = StringField('Departamento', [validators.Length(min=4, max=25)])


class CityForm(Form):
    name = StringField('Ciudad', [validators.Length(min=4, max=25)])


class SeismicForm(Form):
    seismic_date = StringField('Fecha del sismo')
    seismic_time = DateTimeField('Hora del sismo')
    richter_scale = SelectField('Escala de Richter', choices=[
        ('default', ''),

        (   1,   1),
        ( 1.1, 1.1),
        ( 1.2, 1.2),
        ( 1.3, 1.3),
        ( 1.4, 1.4),
        ( 1.5, 1.5),
        ( 1.6, 1.6),
        ( 1.7, 1.7),
        ( 1.8, 1.8),
        ( 1.9, 1.9),

        (   2,   2),
        ( 2.1, 2.1),
        ( 2.2, 2.2),
        ( 2.3, 2.3),
        ( 2.4, 2.4),
        ( 2.5, 2.5),
        ( 2.6, 2.6),
        ( 2.7, 2.7),
        ( 2.8, 2.8),
        ( 2.9, 2.9),

        (   3,   3),
        ( 3.1, 3.1),
        ( 3.2, 3.2),
        ( 3.3, 3.3),
        ( 3.4, 3.4),
        ( 3.5, 3.5),
        ( 3.6, 3.6),
        ( 3.7, 3.7),
        ( 3.8, 3.8),
        ( 3.9, 3.9),

        (   4,   4),
        ( 4.1, 4.1),
        ( 4.2, 4.2),
        ( 4.3, 4.3),
        ( 4.4, 4.4),
        ( 4.5, 4.5),
        ( 4.6, 4.6),
        ( 4.7, 4.7),
        ( 4.8, 4.8),
        ( 4.9, 4.9),

        (  5,   5),
        (5.1, 5.1),
        (5.2, 5.2),
        (5.3, 5.3),
        (5.4, 5.4),
        (5.5, 5.5),
        (5.6, 5.6),
        (5.7, 5.7),
        (5.8, 5.8),
        (5.9, 5.9),

        (   6,   6),
        ( 6.1, 6.1),
        ( 6.2, 6.2),
        ( 6.3, 6.3),
        ( 6.4, 6.4),
        ( 6.5, 6.5),
        ( 6.6, 6.6),
        ( 6.7, 6.7),
        ( 6.8, 6.8),
        ( 6.9, 6.9),

        (   7,   7),
        ( 7.1, 7.1),
        ( 7.2, 7.2),
        ( 7.3, 7.3),
        ( 7.4, 7.4),
        ( 7.5, 7.5),
        ( 7.6, 7.6),
        ( 7.7, 7.7),
        ( 7.8, 7.8),
        ( 7.9, 7.9),

        (8  ,  8),
        (8.1, 8.1),
        (8.2, 8.2),
        (8.3, 8.3),
        (8.4, 8.4),
        (8.5, 8.5),
        (8.6, 8.6),
        (8.7, 8.7),
        (8.8, 8.8),
        (8.9, 8.9),

        (9  ,    9),
        (9.1, 9.1),
        (9.2, 9.2),
        (9.3, 9.3),
        (9.4, 9.4),
        (9.5, 9.5),
        (9.6, 9.6),
        (9.7, 9.7),
        (9.8, 9.8),
        (9.9, 9.9),

        (10, 10),

    ])
    city_id = SelectField("Ciudad",choices=[])
    department = SelectField("Departamento",choices=[])

