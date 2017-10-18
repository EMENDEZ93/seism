from flask import Flask, render_template
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
    user = Country.query.filter_by(name='Colombia').first_or_404()
    return render_template('index.html',user=user)

@app.route('/admin',methods=('GET', 'POST'))
def admin():
    form = CountryForm(request.form)
    user = Country.query.all()

    if request.method == 'POST' and form.validate():
        form = CountryForm(request.form)
        user = Country.query.all()

        if request.method == 'POST' and form.validate():
            country = Country(form.name.data)
            db.session.add(country)
            db.session.commit()

    return render_template('admin/admin.html',user=user,form=form)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()