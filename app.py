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


@app.route('/colombia_cities_local')
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

    return render_template('index.html')


@app.route('/colombia_cities_heroku')
def colombia_cities_data_heroku():

    date   = ["01/01/11","02/01/11","04/01/11","05/01/11","06/01/11","08/01/11","09/01/11","10/01/11","12/01/11","13/01/11","16/01/11","20/01/11","21/01/11","22/01/11","27/01/11","28/01/11","29/01/11","01/02/11","02/02/11","03/02/11","07/02/11","09/02/11","10/02/11","13/02/11","15/02/11","17/02/11","19/02/11","20/02/11","21/02/11","22/02/11","23/02/11","24/02/11","25/02/11","27/02/11","28/02/11","01/03/11","02/03/11","03/03/11","05/03/11","09/03/11","11/03/11","12/03/11","13/03/11","14/03/11","15/03/11","16/03/11","17/03/11","18/03/11","19/03/11","20/03/11","22/03/11","23/03/11","24/03/11","25/03/11","26/03/11","28/03/11","29/03/11","30/03/11","31/03/11","01/04/11","02/04/11","03/04/11","04/04/11","05/04/11","06/04/11","07/04/11","08/04/11","11/04/11","12/04/11","13/04/11","15/04/11","16/04/11","17/04/11","18/04/11","20/04/11","21/04/11","22/04/11","24/04/11","26/04/11","27/04/11","28/04/11","29/04/11","30/04/11","01/05/11",]
    cities = ["Ambalema","Cucunubá","Tumaco","Los Santos","San Cayetano","Francisco Pizarro","Francisco Pizarro","Agustín Codazzi","Los Santos","Los Santos","Valledupar","Valledupar","Los Santos","Cajibío","Los Santos","Los Santos","Trujillo","Nuquí","San Marcos","Obando","Los Santos","Ricaurte","Roberto Payán","Murillo","El Carmen de Chucurí","Gorgona","Francisco Pizarro","Tumaco","San José Del Palmar","Los Santos","Cartagena","Los Santos","Zapatoca","Villanueva","San Pedro","El Calvario","Los Santos","El Águila","Caucasia","Calima","Sutamarchán","Los Santos","Villanueva","Los Santos","Orito","Zaragoza","Gorgona","Los Santos","Los Santos","Rivera","Los Santos","Jordán","Los Santos","Tumaco","Los Santos","Mosquera","Puerto Rico","Puerto Rico","Briceño","Ituango","Los Santos","Riosucio","San José Del Palmar","Buenaventura","El Tablón","Sipí","Los Santos","Villanueva","Los Santos","Los Santos","Tumaco","Los Santos","Cúcuta","Los Santos","Necoclí","Iles","Iles","El Charco","Los Santos","Los Santos","El Bagre","Los Santos","Bolivar","Tamalameque",]
    time   = ["00:02:04","11:29:15","16:38:02","00:33:40","03:18:02","16:14:35","18:21:56","02:40:30","22:09:30","11:04:43","22:09:44","02:02:01","02:44:55","03:55:10","00:55:10","01:06:03","07:09:15","11:42:19","15:34:29","07:00:37","01:10:51","01:20:47","21:24:57","08:38:40","09:50:18","12:53:42","02:33:43","12:46:20","07:51:01","03:29:04","19:58:13","20:27:39","04:18:59","12:32:54","13:12:31","14:06:47","23:39:04","00:05:17","03:09:41","07:13:41","10:23:48","11:23:25","03:35:33","10:25:38","11:35:09","11:23:40","11:50:29","00:02:55","19:21:50","10:02:51","06:15:36","19:13:48","09:58:51","12:51:39","15:56:43","00:45:18","06:51:45","06:57:38","09:22:07","10:07:46","10:18:21","09:00:49","04:01:25","06:43:28","03:11:39","11:31:25","17:01:56","05:31:47","15:10:39","03:23:53","19:38:34","08:27:31","13:55:45","02:41:08","18:50:49","07:43:01","07:57:46","06:38:00","08:27:15","17:35:17","03:56:35","20:13:24","08:48:46","09:23:19",]
    grade  = ["3.1","3.2","2.9","3.5","1.8","3.3","2.7","2.5","3.1","4.5","2.8","2.3","3.3","2.8","3.2","3.5","3.9","3","2.4","3.1","4","2.3","2.2","3","4","4.3","2.1","1.6","3.4","3.4","3.6","3.8","4.1","3.4","3.4","4","4.1","4.3","2.4","4.6","3.8","3.4","3.2","3.4","3.6","2.4","2.9","3.5","3.4","4.1","3.2","3.3","3.8","2.8","2.9","2.2","3.1","3.5","2.8","3.2","4.1","3.4","2.9","2.6","2.5","4.4","4.0","3.1","3.5","3.6","3.1","3.5","3.6","3.5","5.2","2.1","2","2.4","3.1","3.5","2","3.6","2.9","3.9",]

    for index in range(0,len(date)):
        cityFound = City.query.filter_by(name=cities[index]).first()
        if cityFound:
            seismFound = Seism.query.filter_by(city_id=cityFound.id, seismic_date=date[index], seismic_time=time[index], richter_scale=float( grade[index] ) ).first()
            if not seismFound:
                datetime_ = date[index]
                time_ = time[index]
                date_ = float(grade[index])
                seism = Seism(time_, datetime_, date_, cityFound.id)
                db.session.add(seism)
                db.session.commit()

    return render_template('index.html')


@app.route("/arduino/<name_country>",methods=['GET','POST'])
def arduino(name_country):

    if request.method == 'GET':
        country = Country(name_country)
        db.session.add(country)
        db.session.commit()
        return 'Save...'

    return 'Load....without save'



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