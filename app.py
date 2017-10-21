# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms.ext.appengine.db import model_form
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result, Country, Department
from forms import CountryForm, DepartmentForm


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/admin',methods=('GET', 'POST'))
def new_country():
    form = CountryForm(request.form)
    countries = Country.query.all()

    if request.method == 'POST' and form.validate():
        country = Country(form.name.data)
        db.session.add(country)
        db.session.commit()
        return redirect(url_for('new_country'))

    return render_template('admin/country/form.html', countries=countries, form=form)

@app.route("/edit/country/<id_country>",methods=['GET','POST'])
def edit_country(id_country):
    country = Country.query.get_or_404(id_country)
    form = CountryForm(request.form)

    if form.validate():
        country.name = form.name.data
        db.session.commit()
        return redirect(url_for('new_country'))

    form.name.data = country.name
    return render_template('admin/country/form.html',form=form)


@app.route('/country/<int:id_country>',methods=['GET','POST','DELETE'])
def delete_country(id_country):
    if request.method == 'POST' or request.method == 'DELETE':
        country = Country.query.filter_by(id=id_country).first_or_404()
        db.session.delete(country)
        db.session.commit()

    return redirect(url_for('new_country'))


@app.route('/country/<name_country>/department',methods=('GET', 'POST'))
def new_department(name_country):
    form = DepartmentForm(request.form)
    country = Country.query.filter_by(name=name_country).first_or_404()
    departments = Department.query.filter_by(country_id=country.id).order_by(Department.name).all()

    if country:
        if request.method == 'POST' and form.validate():
            department = Department(form.name.data,country.id)
            db.session.add(department)
            db.session.commit()
            return redirect(url_for('new_department',name_country=country.name))

    return render_template('admin/department/form.html', country=country, form=form, departments=departments)


@app.route('/colombia')
def colombia_departments_data():
    country = Country.query.filter_by(name="Colombia").first()
    if not country:
        country_ = Country('Colombia')
        db.session.add(country_)
        db.session.commit()
        country = Country.query.filter_by(name="Colombia").first()

    departments={'Amazonas', 'Antioquia', 'Arauca', 'Atlántico', 'Bolívar', 'Boyacá', 'Caldas', 'Caquetá', 'Casanare',
                 'Cauca', 'Cesar', 'Chocó', 'Córdoba', 'Cundinamarca', 'Guainía', 'Guaviare', 'Huila', 'Guajira',
                 'Magdalena', 'Meta', 'Nariño', 'Norte de Santander', 'Putumayo', 'Quindío', 'Risaralda',
                 'San Andrés y Providencia', 'Santander', 'Sucre', 'Tolima', 'Valle del Cauca', 'Vaupés', 'Vichada',}

    for department in departments:
        department_validate = Department.query.filter_by(name=department).first()
        if not department_validate:
            if country:
                department_ = Department(department,country.id)
                db.session.add(department_)
                db.session.commit()

    return render_template('index.html')


@app.route("/country/<name_country>/department/<int:id_department>'",methods=['GET','POST'])
def edit_department(name_country,id_department):
    country = Country.query.filter_by(name=name_country).first_or_404()
    department = Department.query.filter_by(id=id_department).first_or_404()
    form = DepartmentForm(request.form)

    if form.validate() and department and country:
        department.name = form.name.data
        db.session.commit()
        return redirect(url_for('new_department', name_country=country.name))

    form.name.data = department.name
    return render_template('admin/department/form.html',form=form, country=country)



@app.route('/department/<int:id_department>',methods=['GET','POST','DELETE'])
def delete_department(id_department):
    if request.method == 'POST' or request.method == 'DELETE':
        department = Department.query.filter_by(id=id_department).first_or_404()
        country = Country.query.filter_by(id=department.country_id).first_or_404()
        db.session.delete(department)
        db.session.commit()

    return redirect(url_for('new_department',name_country=country.name))


if __name__ == '__main__':
    app.run()