# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import openpyxl

from decimal import *
from datetime import datetime
from wtforms import Form
from wtforms.ext.appengine.db import model_form
from flask import Flask, render_template, redirect, url_for, json, jsonify
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Country, Department, City, Seism
from forms import CountryForm, DepartmentForm, CityForm, SeismicForm


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


@app.route('/colombia_departments')
def colombia_departments_data():
    country = Country.query.filter_by(name="Colombia").first()
    if not country:
        country_ = Country('Colombia')
        db.session.add(country_)
        db.session.commit()
        country = Country.query.filter_by(name="Colombia").first()

    departments={'Amazonas', 'Antioquia', 'Arauca', 'Atlántico', 'Boyacá', 'Bolívar', 'Caldas', 'Caquetá', 'Casanare',
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

    cities = {}
    cities["Amazonas"]=[
    "Puerto Nariño",
    "Leticia",]
    cities["Antioquia"]=[
    "Medellín",
    "Abejorral",
    "Abriaqui",
    "Alejandría",
    "Amagá",
    "Amalfi",
    "Andes",
    "Angelópolis",
    "Angostura",
    "Anorí",
    "Anzá",
    "Apartadó",
    "Arboletes",
    "Argelia",
    "Armenia",
    "Barbosa",
    "Belmira",
    "Bello",
    "Betania",
    "Betulia",
    "Bolívar",
    "Briceño",
    "Buriticá",
    "Cáceres",
    "Caicedo",
    "Caldas",
    "Campamento",
    "Cañasgordas",
    "Caracolí",
    "Caramanta",
    "Carepa",
    "Carmen de Viboral",
    "Carolina",
    "Caucasia",
    "Chigorodó",
    "Cisneros",
    "Cocorná",
    "Concepción",
    "Concordia",
    "Copacabana",
    "Dabeiba",
    "Don Matías",
    "Ebéjico",
    "El Bagre",
    "Entrerríos",
    "Envigado",
    "Fredonia",
    "Frontino",
    "Giraldo",
    "Girardota",
    "Gómez Plata",
    "Granada",
    "Guadalupe",
    "Guarne",
    "Guatapé",
    "Heliconia",
    "Hispania",
    "Itagüí",
    "Ituango",
    "Jardín",
    "Jericó",
    "La Ceja",
    "La Estrella",
    "La Pintada",
    "La Unión",
    "Liborina",
    "Maceo",
    "Marinilla",
    "Montebello",
    "Murindó",
    "Mutatá",
    "Nariño",
    "Necoclí",
    "Nechí",
    "Olaya",
    "Peñol",
    "Peque",
    "Pueblorrico",
    "Puerto Berrío",
    "Puerto Nare",
    "Puerto Triunfo",
    "Remedios",
    "Retiro",
    "Rionegro",
    "Sabanalarga",
    "Sabaneta",
    "Salgar",
    "San Andrés",
    "San Carlos",
    "San francisco",
    "San Jerónimo",
    "San José de Montaña",
    "San Juan de Urabá",
    "San Luis",
    "San Pedro",
    "San Pedro de Urabá",
    "San Rafael",
    "San Roque",
    "San Vicente",
    "Santa Bárbara",
    "Santa Rosa de Osos",
    "Santo Domingo",
    "Santuario",
    "Segovia",
    "Sonsón",
    "Sopetrán",
    "Támesis",
    "Tarazá",
    "Tarso",
    "Titiribí",
    "Toledo",
    "Turbo",
    "Uramita",
    "Urrao",
    "Valdivia",
    "Valparaíso",
    "Vegachí",
    "Venecia",
    "Vigía del Fuerte",
    "Yalí",
    "Yarumal",
    "Yolombó",
    "Yondó",
    "Zaragoza",]
    cities["Arauca"]=[
    "Arauca",
    "Arauquita",
    "Cravo Norte",
    "Fortul",
    "Puerto Rondón",
    "Fortul",
    "Puerto Rondón",
    "Saravena",
    "Tame",]
    cities["Atlántico"]=[
    "Barranquilla",
    "Baranoa",
    "Campo de la Cruz",
    "Candelaria",
    "Galapa",
    "Juan de Acosta",
    "Luruaco",
    "Malambo",
    "Manatí",
    "Palmar de Varela",
    "Piojó",
    "Polonuevo",
    "Ponedera",
    "Puerto Colombia",
    "Repelón",
    "Sabanagrande",
    "Sabanalarga",
    "Santa Lucía",
    "Santo Tomás",
    "Soledad",
    "Suán",
    "Tubará",
    "Usiacurí",
    "Cartagena",
    "Achí",
    "Altos del Rosario",
    "Arenal",
    "Arjona",
    "Arroyohondo",
    "Barranco de Loba",
    "Calamar",
    "Cantagallo",
    "Cicuto",
    "Córdoba",
    "Clemencia",
    "El Carmen de Bolívar",
    "El Guamo",
    "El Peñón",
    "Hatillo de Loba",
    "Magangue",
    "Mahates",
    "Margarita",
    "María la Baja",
    "Montecristo",
    "Mompós",
    "Morales",
    "Pinillos",
    "Regidor",
    "Río Viejo",
    "San Cristóbal",
    "San Estanislao",
    "San Fernando",
    "San Jacinto",
    "San Jacinto del Cauca",
    "San Juan Nepomuceno",
    "San Martín de Loba",
    "San Pablo",
    "Santa Catalina",
    "Santa Rosa",
    "Santa Rosa del Sur",
    "Simití",
    "Soplaviento",
    "Talaigua Nuevo",
    "Tiquisio",
    "Turbaco",
    "Turbaná",
    "Villanueva",
    "Zambrano",]
    cities["Boyacá"]=[
    "Tunja",
    "Almeida",
    "Aquitania",
    "Arcabuco",
    "Belén",
    "Berbeo",
    "Beteitiva",
    "Boavita",
    "Briseño",
    "Buenavista",
    "Busbanzá",
    "Caldas",
    "Campohermoso",
    "Cerinza",
    "Chinavita",
    "Chiquinquirá",
    "Chiscas",
    "Chita",
    "Chitaranque",
    "Chivatá",
    "Ciénaga",
    "Cómbita",
    "Coper",
    "Corrales",
    "Covarachia",
    "Cubar",
    "Cubará",
    "Cucaita",
    "Cuitiva",
    "Chíquiza",
    "Chivor",
    "Duitama",
    "El Cocuy",
    "El Espino",
    "Firavitoba",
    "Floresta",
    "Gachantivá",
    "Gámeza",
    "Garagoa",
    "Guacamayas",
    "Guateque",
    "Guayatá",
    "Guicán",
    "Iza",
    "Jenesano",
    "Jericó",
    "Labranzagrande",
    "La Capilla",
    "La Victoria",
    "La Ubita",
    "Villa de Leyva",
    "Macanal",
    "Maripí",
    "Miraflores",
    "Mongua",
    "Monguí",
    "Moniquirá",
    "Motavita",
    "Muzo",
    "Nobsa",
    "Nuevo Colón",
    "Oicatá",
    "Otanche",
    "Pachavita",
    "Páez",
    "Paipa",
    "Pajarito",
    "Panqueba",
    "Pauna",
    "Paya",
    "Paz de Río",
    "Pesca",
    "Pisva",
    "Puerto Boyacá",
    "Quípama",
    "Ramiquirí",
    "Ráquira",
    "Rondón",
    "Saboyá",
    "Sáchica",
    "Samacá",
    "San Eduardo",
    "San José de Pare",
    "San Luis de Gaceno",
    "San Mateo",
    "San Miguel de Sema",
    "San Pablo de Borbur",
    "Santana",
    "Santa María",
    "Santa Rosa de Viterbo",
    "Santa Sofía",
    "Sativanorte",
    "Sativasur",
    "Siachoque",
    "Soatá",
    "Socotá",
    "Socha",
    "Sogamoso",
    "Somondoco",
    "Sora",
    "Sotaquirá",
    "Soracá",
    "Susacón",
    "Sutamarchán",
    "Sutatenza",
    "Tasco",
    "Tenza",
    "Tibaná",
    "Tibasosa",
    "Tinjacá",
    "Tipacoque",
    "Toca",
    "Toguí",
    "Tópaga",
    "Tota",
    "Tunungua",
    "Turmequé",
    "Tuta",
    "Tutazá",
    "Úmbita",
    "Ventaquemada",
    "Viracachá",
    "Zetaquirá",]
    cities["Bolívar"] = [
        "Pinillos",
        "Cartagena",
        "Santa Rosa de Lima",
        "Santa Catalina", ]
    cities["Caldas"]=[
    "Manizales",
    "Aguadas",
    "Anserma",
    "Aranzazu",
    "Belalcázar",
    "Chinchina",
    "Filadelfia",
    "La Dorada",
    "La Merced",
    "Manzanares",
    "Marmato",
    "Marquetalia",
    "Marulanda",
    "Neira",
    "Norcasia",
    "Pácora",
    "Palestina",
    "Pensilvania",
    "Riosucio",
    "Risaralda",
    "Salamina",
    "Samaná",
    "San José",
    "Supía",
    "Victoria",
    "Villamaría",
    "Viterbo",]
    cities["Caquetá"]=[
    "Florencia",
    "Albania",
    "Belén de los Andaquíes",
    "Cartagena del Chairá",
    "Curillo",
    "El Doncello",
    "El Paujil",
    "La Montañita",
    "Milán",
    "Morelia",
    "Puerto Rico",
    "San José del Fragua",
    "San Vicente del Caguán",
    "Solano",
    "Solita",
    "Valparaíso",]
    cities["Casanare"]=[
    "Yopal",
    "Aguazul",
    "Chameza",
    "Hato Corozal",
    "La Salina",
    "Maní",
    "Monterrey",
    "Nunchía",
    "Orocué",
    "Paz de Ariporo",
    "Pore",
    "Recetor",
    "Sabalarga",
    "Sácama",
    "San Luis de Palenque",
    "Támara",
    "Tauramena",
    "Trinidad",
    "Villanueva",]
    cities["Cauca"]=[
    "Popayán",
    "Almaguer",
    "Argelia",
    "Balboa",
    "Bolívar",
    "Buenos Aires",
    "Cajibío",
    "Caldono",
    "Caloto",
    "Gorgona",
    "Corinto",
    "El Tambo",
    "Florencia",
    "Guapi",
    "Inzá",
    "Jambaló",
    "La Sierra",
    "La Vega",
    "López",
    "Mercaderes",
    "Miranda",
    "Morales",
    "Padilla",
    "Páez",
    "Patía",
    "Piamonte",
    "Piendamó",
    "Puerto Tejada",
    "Puracé",
    "Rosas",
    "San Sebastián",
    "Santander de Quilichao",
    "Santa Rosa",
    "Silvia",
    "Sotará",
    "Suárez",
    "Timbío",
    "Timbiquí",
    "Toribío",
    "Totoro",]
    cities["Cesar"]=[
    "Valledupar",
    "Aguachica",
    "Agustín Codazzi",
    "Astrea",
    "Becerril",
    "Bosconia",
    "Chimichagua",
    "Chiriguaná",
    "Curumaní",
    "El Copey",
    "El Paso",
    "Gamarra",
    "González",
    "La Gloria",
    "La Jagua de Ibirico",
    "Manaure Balcón Cesar",
    "Pailitas",
    "Pelaya",
    "Pueblo Bello",
    "Río de Oro",
    "La Paz",
    "San Alberto",
    "San Diego",
    "San Martín",
    "Tamalameque",]
    cities["Córdoba"]=[
    "Montería",
    "Ayapel",
    "Buenavista",
    "Canalete",
    "Cereté",
    "Chima",
    "Chinú",
    "Ciénaga de Oro",
    "Cotorra",
    "La Apartada",
    "Lorica",
    "Los Córdobas",
    "Momil",
    "Montelíbano",
    "Monitos",
    "Planeta Rica",
    "Pueblo Nuevo",
    "Puerto Escondido",
    "Puerto Libertador",
    "Purísima",
    "Sahagún",
    "San Andrés Sotavento",
    "San Antero",
    "San Bernardo del Viento",
    "San Carlos",
    "San Pelayo",
    "Tierralta",
    "Valencia",]
    cities["Cundinamarca"]=[
    "Agua de Dios",
    "Albán",
    "Anapoima",
    "Anolaima",
    "Arbeláez",
    "Beltrán",
    "Bituima",
    "Bojacá",
    "Cabrera",
    "Cachipay",
    "Cajicá",
    "Caparrapí",
    "Cáqueza",
    "Carmen de Carupa",
    "Chaguaní",
    "Chía",
    "Chipaque",
    "Choachí",
    "Chocontá",
    "Cogua",
    "Cota",
    "Cucunubá",
    "El Colegio",
    "El Peñón",
    "El Rosal",
    "Facatativá",
    "Fómeque",
    "Fosca",
    "Funza",
    "Fúquene",
    "Fusagasugá",
    "Gachalá",
    "Gachancipá",
    "Gachetá",
    "Gama",
    "Girardot",
    "Granada",
    "Guachetá",
    "Guaduas",
    "Guasca",
    "Guataquí",
    "Guatavita",
    "Guayabal de Síquima",
    "Guayabetal",
    "Gutiérrez",
    "Jerusalén",
    "Junín",
    "La Calera",
    "La Mesa",
    "La Palma",
    "La Peña",
    "La Vega",
    "Lenguazaque",
    "Machetá",
    "Madrid",
    "Manta",
    "Medina",
    "Mosquera",
    "Nariño",
    "Nemocón",
    "Nilo",
    "Nimaima",
    "Nocaima",
    "Venecia",
    "Pacho",
    "Paime",
    "Pandi",
    "Paratebueno",
    "Pasca",
    "Puerto Salgar",
    "Pulí",
    "Quebradanegra",
    "Quetame",
    "Quipile",
    "Rafael",
    "Ricaurte",
    "San Antonio de Tequendama",
    "San Bernardo",
    "San Cayetano",
    "San Francisco",
    "San Juan de Rioseco",
    "Sasaima",
    "Sesquilé",
    "Sibate",
    "Silvania",
    "Simijaca",
    "Soacha",
    "Sopó",
    "Subachoque",
    "Suesca",
    "Supatá",
    "Susa",
    "Sutatausa",
    "Tabio",
    "Tausa",
    "Tena",
    "Tenjo",
    "Tibacuy",
    "Tibiritá",
    "Tocaima",
    "Tocancipá",
    "Topaipí",
    "Ubalá",
    "Ubaque",
    "Ubaté",
    "Une",
    "Útica",
    "Vergara",
    "Vianí",
    "Villagómez",
    "Villapinzón",
    "Villeta",
    "Viotá",
    "Yacopí",
    "Zipacón",
    "Zipaquirá",]
    cities["Chocó"]=[
    "Quibdó",
    "Acandí",
    "Alto Baudó",
    "Atrato",
    "Bagadó",
    "Bahía Solano",
    "Bajo Baudó",
    "Bojayá",
    "Cantón de San Pablo",
    "Condoto",
    "El Carmen",
    "El Litoral de San Juan",
    "Itsmina",
    "Juradó",
    "Lloró",
    "Nóvita",
    "Nuquí",
    "Riosucio",
    "San José Del Palmar",
    "Sipí",
    "Tadó",
    "Unguía",]
    cities["Guainía"]=[
    "Puerto Inírida",]
    cities["Guaviare"]=[
    "San José del Guaviare",
    "Calamar",
    "El Retorno",
    "Miraflores",]
    cities["Huila"]=[
    "Neiva",
    "Acevedo",
    "Agrado",
    "Aipe",
    "Algeciras",
    "Altamira",
    "Baraya",
    "Campoalegre",
    "Colombia",
    "Elias",
    "Garzón",
    "Gigante",
    "Guadalupe",
    "Hobo",
    "Iquira",
    "Isnos",
    "La Argentina",
    "La Plata",
    "Nátaga",
    "Oporapa",
    "Paicol",
    "Palermo",
    "Palestina",
    "Pital",
    "Pitalito",
    "Rivera",
    "Saladoblanco",
    "San Agustín",
    "Santa María",
    "Suazá",
    "Tarqui",
    "Tesalia",
    "Tello",
    "Teruel",
    "Timaná",
    "Villavieja",
    "Yaguará",
    "Volcán Nevado del Huila",]
    cities["Guajira"]=[
    "Riohacha",
    "Barrancas",
    "Dibulla",
    "Distracción",
    "El Molino",
    "Fonseca",
    "Hatonuevo",
    "Maicao",
    "Manaure",
    "San Juan del Cesar",
    "Uribía",
    "Urumita",
    "Villanueva",]
    cities["Magdalena"]=[
    "Santa Marta",
    "Aracataca",
    "Ariguaní",
    "Cerro San Antonio",
    "Chivolo",
    "Ciénaga",
    "El Banco",
    "El Piñón",
    "El Retén",
    "Fundación",
    "Guamal",
    "Pedraza",
    "Pijiño del Carmen",
    "Pivijay",
    "Plato",
    "Publoviejo",
    "Remolino",
    "Salamina",
    "San Sebastián de Buuenavista",
    "San Juan De Río Seco",
    "San Zenón",
    "Santa Ana",
    "Sitionuevo",
    "Tenerife",]
    cities["Meta"]=[
    "Villavicencio",
    "Acacias",
    "Barranca de Upía",
    "Cabuyaro",
    "Castilla la Nueva",
    "Cubarral",
    "Cumaral",
    "El Calvario",
    "El Castillo",
    "El Dorado",
    "Fuente de Oro",
    "Granada",
    "Guamal",
    "Mapiripán",
    "Mesetas",
    "La Macarena",
    "La Uribe",
    "Lejanías",
    "Puerto Concordia",
    "Puerto Gaitán",
    "Puerto López",
    "Puerto Lleras",
    "Puerto Rico",
    "Restrepo",
    "San Carlos de Guaroa",
    "San Juan de Arama",
    "San Juanito",
    "San Martín",
    "Vistahermosa",]
    cities["Nariño"]=[
    "Pasto",
    "Albán",
    "Aldana",
    "Ancuyá",
    "Arboleda",
    "Barbacoas",
    "Belén",
    "Buesaco",
    "Colón",
    "Consacá",
    "Contadero",
    "Córdoba",
    "Cuaspud",
    "Cumbal",
    "Cumbitará",
    "Chachaguí",
    "El Charco",
    "El Rosario",
    "El Tablón",
    "El Tambo",
    "Funes",
    "Guachucal",
    "Guaitarilla",
    "Gualmatán",
    "Iles",
    "Imúes",
    "Ipiales",
    "La Cruz",
    "La Florida",
    "La Llanada",
    "La Tola",
    "La Unión",
    "Leiva",
    "Linares",
    "Los Andes",
    "Magüí",
    "Mallama",
    "Mosquera",
    "Olaya",
    "Ospina",
    "Francisco Pizarro",
    "Policarpa",
    "Potosí",
    "Providencia",
    "Puerres",
    "Pupiales",
    "Ricaurte",
    "Roberto Payán",
    "Samaniego",
    "Sandoná",
    "San Bernardo",
    "San Lorenzo",
    "San Pablo",
    "San Pedro de Cartago",
    "Santa Bárbara",
    "Santa Cruz",
    "Sapuyés",
    "Taminango",
    "Tangua",
    "Tumaco",
    "Túquerres",
    "Yacuanquer",
    "Volcán Galeras",]
    cities["Norte de Santander"]=[
    "Cúcuta",
    "Abrego",
    "Arboledas",
    "Bochalema",
    "Bucarasica",
    "Cácota",
    "Cáchira",
    "Chinácota",
    "Chitagá",
    "Convención",
    "Cucutilla",
    "Durania",
    "El Carmen",
    "El Tarra",
    "El Zulia",
    "Gramalote",
    "Hacarí",
    "Herrán",
    "Labateca",
    "La Esperanza",
    "La Playa",
    "Los Patios",
    "Lourdes",
    "Mutiscua",
    "Ocaña",
    "Pamplona",
    "Pamplonita",
    "Puerto Santander",
    "Ragonvalia",
    "Salazar",
    "San Calixto",
    "San Cayetano",
    "Santiago",
    "Sardinata",
    "Silos",
    "Teorama",
    "Tibú",
    "Toledo",
    "Villacaro",
    "Villa del Rosario",]
    cities["Putumayo"]=[
    "Mocoa",
    "Colón",
    "Orito",
    "Puerto Asís",
    "Puerto Caicedo",
    "Puerto Guzmán",
    "Puerto Leguízamo",
    "Sibundoy",
    "San Francisco",
    "San Miguel",
    "Santiago",
    "Villa Gamuez",
    "Villagarzón",]
    cities["Quindío"]=[
    "Armenia",
    "Buenavista",
    "Calarcá",
    "Circasia",
    "Córdoba",
    "Filandia",
    "Génova",
    "La Tebaida",
    "Montenegro",
    "Pijao",
    "Quimbaya",
    "Salento",]
    cities["Risaralda"]=[
    "Pereira",
    "Apía",
    "Balboa",
    "Belén de Umbría",
    "Dos Quebradas",
    "Guática",
    "La Celia",
    "La Virginia",
    "Marsella",
    "Mistrató",
    "Pueblo Rico",
    "Quinchia",
    "Santa Rosa de Cabal",
    "Santuario",]
    cities["San Andrés y Providencia"]=[
    "San Andrés",
    "Providencia",]
    cities["Santander"]=[
    "Bucaramanga",
    "Aguada",
    "Albania",
    "Aratoca",
    "Barbosa",
    "Barichara",
    "Barrancabermeja",
    "Betulia",
    "Bolívar",
    "Cabrera",
    "California",
    "Capitanejo",
    "Carcasí",
    "Cepitá",
    "Cerrito",
    "Charalá",
    "Charta",
    "Chima",
    "Chipatá",
    "Cimitarra",
    "Concepción",
    "Confines",
    "Contratación",
    "Coromoro",
    "Curití",
    "El Carmen de Chucurí",
    "El Guacamayo",
    "El Peñón",
    "El Playón",
    "Encino",
    "Enciso",
    "Florián",
    "Floridablanca",
    "Galán",
    "Gámbita",
    "Girón",
    "Guaca",
    "Guadalupe",
    "Guapotá",
    "Guavatá",
    "Guepsa",
    "Hato",
    "Jesús María",
    "Jordán",
    "La Belleza",
    "Landázuri",
    "La Paz",
    "Lebrija",
    "Los Santos",
    "Macaravita",
    "Málaga",
    "Matanza",
    "Mogotes",
    "Molagavita",
    "Ocamonte",
    "Oiba",
    "Onzága",
    "Palmar",
    "Palmas del Socorro",
    "Páramo",
    "Piedecuesta",
    "Pinchote",
    "Puente Nacional",
    "Puerto Parra",
    "Puerto Wilches",
    "Rionegro",
    "Sabana de Torres",
    "San Andrés",
    "San Benito",
    "San Gil",
    "San Joaquín",
    "San José de Miranda",
    "San Miguel",
    "San Vicente de Chucurí",
    "Santa Bárbara",
    "Santa Helena del Opón",
    "Simacota",
    "Socorro",
    "Suaita",
    "Sucre",
    "Suratá",
    "Tona",
    "Valle de San José",
    "Vélez",
    "Vetas",
    "Villanueva",
    "Zapatoca",]
    cities["Sucre"]=[
    "Sincelejo",
    "Buenavista",
    "Caimito",
    "Coloso",
    "Corozal",
    "Chalán",
    "Galeras",
    "Guarandá",
    "La Unión",
    "Los Palmitos",
    "Majagual",
    "Morroa",
    "Ovejas",
    "Palmito",
    "Sampués",
    "San Benito Abad",
    "San Juan de Betulia",
    "San Marcos",
    "San Onofre",
    "San Pedro",
    "Sincé",
    "Tolú",
    "Toluviejo",]
    cities["Tolima"]=[
    "Ibagué",
    "Alpujarra",
    "Alvarado",
    "Ambalema",
    "Anzóategui",
    "Armero",
    "Ataco",
    "Cajamarca",
    "Carmen de Apicalá",
    "Casabianca",
    "Chaparral",
    "Coello",
    "Coyaima",
    "Cunday",
    "Dolores",
    "Espinal",
    "Falán",
    "Flandes",
    "Fresno",
    "Guamo",
    "Herveo",
    "Honda",
    "Icononzo",
    "Lérida",
    "Líbano",
    "Mariquita",
    "Melgar",
    "Murillo",
    "Natagaima",
    "Ortega",
    "Palocabildo",
    "Piedras",
    "Planadas",
    "Prado",
    "Purificación",
    "Rioblanco",
    "Roncesvalles",
    "Rovira",
    "Saldaña",
    "San Antonio",
    "San Luis",
    "Santa Isabel",
    "Suarez",
    "Valle de San Juan",
    "Venadillo",
    "Villahermosa",
    "Villarrica",]
    cities["Valle del Cauca"]=[
    "Cali",
    "Alcalá",
    "Andalucía",
    "Ansermanuevo",
    "Argelia",
    "Bolívar",
    "Buenaventura",
    "Buga",
    "Bugalagrande",
    "Caicedonia",
    "Calima",
    "Candelaria",
    "Cartago",
    "Dagua",
    "El Águila",
    "El Cairo",
    "El Cerrito",
    "El Dovio",
    "Florida",
    "Ginebra",
    "Guacarí",
    "Jamundí",
    "La Cumbre",
    "La Unión",
    "La Victoria",
    "Obando",
    "Malpelo",
    "Palmira",
    "Pradera",
    "Restrepo",
    "Riofrío",
    "Roldanillo",
    "San Pedro",
    "Sevilla",
    "Toro",
    "Trujillo",
    "Tuluá",
    "Ulloa",
    "Versalles",
    "Vijes",
    "Yotoco",
    "Yumbo",
    "Zarzal",]
    cities["Vaupés"]=[
    "Mitú",
    "Carurú",
    "Tatamá",]
    cities["Vichada"]=[
    "Puerto Carreño",
    "La Primavera",
    "Santa Rosalia",
    "Cumaribo",
    ]

    for department in departments:
        department_id = Department.query.filter_by(name=department).first()
        if department_id:
            for city in cities[department]:
                city_validate = City.query.filter_by(name=city).first()
                if not city_validate:
                    city_ = City(city,department_id.id)
                    db.session.add(city_)
                    db.session.commit()

    return render_template('index.html')


@app.route('/colombia_cities')
def colombia_cities_data():

    doc = openpyxl.load_workbook('RNAC_2011.xlsx')
    sheet = doc.active
    for z,date,city,time,seism in sheet['A3':'E940']:
        cityFound = City.query.filter_by(name=city.value,).first()
        if cityFound:
            seismFound = Seism.query.filter_by(city_id=cityFound.id, seismic_date=date.value, seismic_time=str(time.value), richter_scale=seism.value).first()
            if not seismFound:
                print(cityFound)
                datetime_ = date.value
                time_ = time.value
                date_ = float(seism.value)
                seism = Seism(time_, datetime_, date_, cityFound.id)
                db.session.add(seism)
                db.session.commit()

    return 'ok'



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


@app.route('/country/<name_country>/department/<name_department>',methods=['GET', 'POST'])
def new_city(name_country,name_department):
    form = CityForm(request.form)
    country = Country.query.filter_by(name=name_country).first_or_404()
    department = Department.query.filter_by(name=name_department).first_or_404()
    cities = City.query.filter_by(department_id=department.id).order_by(City.name).all()

    if department:
        if request.method == 'POST' and form.validate():
            city = City(form.name.data,department.id)
            db.session.add(city)
            db.session.commit()
            return redirect(url_for('new_city',name_country=country.name,name_department=department.name))

    return render_template('admin/city/form.html', country=country, form=form, department=department, cities=cities)



@app.route("/country/<name_country>/department/<name_department>/city/<int:id_city>",methods=['GET','POST'])
def edit_city(name_country, name_department, id_city):
    form = CityForm(request.form)
    country = Country.query.filter_by(name=name_country).first_or_404()
    department = Department.query.filter_by(name=name_department).first_or_404()
    city = City.query.filter_by(id=id_city).first_or_404()

    if form.validate() and department and country and city:
        city.name = form.name.data
        db.session.commit()
        return redirect(url_for('new_city', name_country=country.name, name_department=department.name))

    form.name.data = city.name
    return render_template('admin/city/form.html', country=country, form=form, department=department)


@app.route('/city/<int:id_city>',methods=['GET','POST','DELETE'])
def delete_city(id_city):
    if request.method == 'POST' or request.method == 'DELETE':
        city = City.query.filter_by(id=id_city).first_or_404()
        department = Department.query.filter_by(id=city.department_id).first_or_404()
        country = Country.query.filter_by(id=department.country_id).first_or_404()
        db.session.delete(city)
        db.session.commit()

    return redirect(url_for('new_city', name_country=country.name, name_department=department.name))


@app.route('/seismic/<name_country>',methods=['GET', 'POST'])
def new_seismic(name_country):
    form = SeismicForm(request.form)
    country = Country.query.filter_by(name=name_country).first()
    department = Department.query.filter_by(country_id =country.id)
    form.department.choices = [(status.id, status.name) for status in department]

    if request.method == 'POST':
        if request.form['seismic_time'] != '' and request.form['seismic_date'] != '' and request.form['richter_scale'] != '' and request.form['city_id'] != '' and request.form['department'] != '':
            city = City.query.filter_by(id=request.form['city_id']).first_or_404()
            if city:
                datetime_ = request.form['seismic_date']
                time_ = request.form['seismic_time']
                date_ = float(request.form['richter_scale'])
                seism = Seism(time_, datetime_, date_, city.id)
                db.session.add(seism)
                db.session.commit()

    return render_template('admin/seismic/form.html', form=form)

@app.route('/get_departments', methods=['POST'])
def get_departments():
    user =  request.form['department']
    department = City.query.filter_by(department_id=int(user)).all()

    city_id={}
    city_name={}
    for department_ in department:
        city_id[str(department_.id)] = department_.id
        city_name[str(department_.id)] = department_.name

    return jsonify({'city_id': city_id,'city_name': city_name});





if __name__ == '__main__':
    app.run()