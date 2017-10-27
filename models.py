from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    country_id = db.Column(db.Integer(), ForeignKey(Country.id))

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    department_id = db.Column(db.Integer(), ForeignKey(Department.id))

    def __init__(self, name, department_id):
        self.name = name
        self.department_id = department_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Seism(db.Model):
    __tablename__ = 'seism'

    id = db.Column(db.Integer, primary_key=True)
    seismic_date = db.Column(db.String())
    seismic_time = db.Column(db.String())
    richter_scale = db.Column(db.Numeric(2,1))
    city_id = db.Column(db.Integer(), ForeignKey(City.id))

    def __init__(self, seismic_time, seismic_date, richter_scale, city_id):
        self.seismic_time =seismic_time
        self.seismic_date =seismic_date
        self.richter_scale =richter_scale
        self.city_id =city_id

    def __repr__(self):
        return '<id {}>'.format(self.id)
