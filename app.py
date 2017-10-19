from flask import Flask, render_template, redirect, url_for
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result, Country
from forms import CountryForm


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/admin',methods=('GET', 'POST'))
def new_country():
    form = CountryForm(request.form)
    countries = Country.query.all()

    if request.method == 'POST' and form.validate():
        form = CountryForm(request.form)
        if request.method == 'POST' and form.validate():
            country = Country(form.name.data)
            db.session.add(country)
            db.session.commit()
            return redirect(url_for('new_country'))

    return render_template('admin/admin.html',countries=countries,form=form)

@app.route('/country/<int:id_country>',methods=['GET','POST','DELETE'])
def delete_country(id_country):
    if request.method == 'POST' or request.method == 'DELETE':
        country = Country.query.filter_by(id=id_country).first_or_404()
        db.session.delete(country)
        db.session.commit()

    return redirect(url_for('new_country'))

if __name__ == '__main__':
    app.run()