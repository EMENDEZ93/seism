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

    def get_all_departments(self):
        department = Department.query.filter_by(country_id=self.id).order_by(Department.name).all()
        return department


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

    def seism_for_department(self):
        n_seism = 0
        for city in City.query.filter_by(department_id =self.id).all():
            n_seism = n_seism + Seism.query.filter_by(city_id =city.id).count()

        return n_seism



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

    def his_seism(self):
        seism = Seism.query.filter_by(city_id=self.id).all()
        return seism

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

    def get_city(self):
        city = City.query.filter_by(id=self.city_id).first()
        return city.name

    def get_department(self):
        city = City.query.filter_by(id=self.city_id).first()
        department = Department.query.filter_by(id=city.department_id).first()
        return department.name

