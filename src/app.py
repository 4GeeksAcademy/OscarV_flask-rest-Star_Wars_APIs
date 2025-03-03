"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People , Favorite_Planet , Favorite_People
#from models import Person

# 1> pipenv run migrate # (to make the migrations)
# 2> pipenv run upgrade  # (to update your databse with the migrations)
#

# https://redesigned-journey-pjp6gxqv494737x5w-3000.app.github.dev/user

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    user =User.query.get(1) # Para llamar solo un objeto...
    #print(user.serialize()) # Aqui imprimo el objeto en consola
    
    response_body = {
        "msg": "GET / People for this project",
        "user": user.serialize() 
    }
    return jsonify(response_body), 200

#-------------------------------------------------PLANET------------------------------------------------#
#-------------------------------------GET-----ALL PLANET------------------------------------------------#
@app.route('/planet', methods=['GET'])
def get_planet():
    list_planets = Planet.query.all()
    obj_all_planets = [planet.serialize() for planet in list_planets]
    #print(all_planets)
    
    response_body = {
        "msg": "GET / Planets for this project",
        "planets": obj_all_planets   # salida de all Planets
    }
    return jsonify(response_body), 200
#----------------------------------GET------1 ID----------------------------------------------------------#
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet_one =Planet.query.get(planet_id)
    print(planet_one.serialize()) 
    
    response_body = {
        "msg": "GET / Solo 1 planeta",
        "Planet": planet_one.serialize() 
    }

    return jsonify(response_body), 200

#-------------------------------------------------PEOPLE------------------------------------------------#
#-------------------------------------GET-----ALL PEOPLE------------------------------------------------#
@app.route('/people', methods=['GET'])
def get_people():
    list_person = People.query.all()
    obj_all_people = [people.serialize() for people in list_person]
    #print(all_people)
    
    response_body = {
        "People":obj_all_people
    }
    return jsonify(response_body), 200
#----------------------------------GET------1 ID----------------------------------------------------------#
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person_ask =People.query.get(people_id) # Para llamar solo un objeto...
    print(person_ask.serialize()) 
    
    response_body = {
        "msg": "GET / Solo 1 persona",
        "user": person_ask.serialize() 
    }

    return jsonify(response_body), 200

#-------------------------------------------------POST------------------------------------------------#
#-------------------------------------POST-----NEW PLANET-------------------------------------------------#
@app.route('/planet', methods=['POST'])
def post_planet():
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    if not data:
         raise APIException('No se proporcionaron datos', status_code=400)
    if 'name' not in data:
         raise APIException('El campo "name" es requerido', status_code=400)
    if data["name"]=="":
        raise APIException('El campo "name" es requerido', status_code=400)

    # siempre tiene que haber data dentro de los corchetes.
    new_planet = Planet(
        name=data["name"],
        rotation_period=data["rotation_period"],
        orbital_period=data["orbital_period"],
        diameter=data["diameter"],
        climate=data["climate"],
        terrain=data["terrain"],
        population=data["population"]
    )

    # Guardar el nuevo planeta en la base de datos
    db.session.add(new_planet)
    db.session.commit()

    # Devolver una respuesta con el planeta creado
    response_body = {
        "msg": f"El nuevo planeta creado es: {new_planet.name}",
        "new_planet": new_planet.serialize() 
        }
    return jsonify(response_body), 201

#-------------------------------------POST-----NEW PEOPLE-------------------------------------------------#
@app.route('/people', methods=['POST'])
def post_people():
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    if not data:
         raise APIException('No se proporcionaron datos', status_code=400)
    if 'name' not in data:
         raise APIException('El campo "name" es requerido', status_code=400)
    if data["name"]=="":
        raise APIException('El campo "name" es requerido', status_code=400)
    if data["planet_id"]=="":
        raise APIException('El campo "Planet_ID" es requerido', status_code=400)

    # siempre tiene que haber data dentro de los corchetes.
    new_person = People(
        name=data["name"],
        height=data["height"],
        hair_color=data["hair_color"],
        skin_color=data["skin_color"],
        eye_color=data["eye_color"],
        birth_year=data["birth_year"],
        gender=data["gender"],
        planet_id=data["planet_id"]
        #planet_id=data.get("planet_id") --get..pero no seria necesario...
    )
    # Guardar el nuevo planeta en la base de datos
    db.session.add(new_person)
    db.session.commit()

    # Devolver una respuesta con el planeta creado
    response_body = {
        "msg": f"El nuevo personaje creado es: {new_person.name}",
        "new_person": new_person.serialize() 
        }
    return jsonify(response_body), 201

#-------------------------------------POST-----FAVORITOS ---PLANET-------------------------------------------------#
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet():
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    if not data:
         raise APIException('No se proporcionaron datos', status_code=400)
    if 'planet_id' not in data:
         raise APIException('El campo "planet_id" es requerido', status_code=400)
    if data["planet_id"]=="":
        raise APIException('El campo "planet_id" es requerido', status_code=400)

    new_favorite_planet = Favorite_Planet(
    user_id=data["user_id"],
    planet_id=data["planet_id"]
)
    
    # Guardar el nuevo planeta en la base de datos
    db.session.add(new_favorite_planet)
    db.session.commit()

    # Devolver una respuesta con el planeta creado
    response_body = {
        "msg": f"El nuevo planeta creado es: {new_favorite_planet.planet_id}",
        "new_Popular_planet": new_favorite_planet.serialize() 
        }
    return jsonify(response_body), 201


#-------------------------------------GET-----ALL FAVORITE PLANET------------------------------------------------#
#https://redesigned-journey-pjp6gxqv494737x5w-3000.app.github.dev/favorite/planet

@app.route('/favorite/planet', methods=['GET'])
def get_favorite_planet():
    list_favorite_planet = Favorite_Planet.query.all()
    obj_favorite_planet = [favorite.serialize() for favorite in list_favorite_planet]
    #print(obj_favorite_planet)
    
    response_body = {
        "Favorite_planet":obj_favorite_planet
    }
    return jsonify(response_body), 200

#-------------------------------------POST-----FAVORITOS ---PEOPLE-------------------------------------------------#

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people():
    data = request.get_json()

    # Validar que los datos necesarios estén presentes
    if not data:
         raise APIException('No se proporcionaron datos', status_code=400)
    if 'people_id' not in data:
         raise APIException('El campo "people_id" es requerido', status_code=400)
    if data["people_id"]=="":
        raise APIException('El campo "people_id" es requerido', status_code=400)

    new_favorite_people = Favorite_People(
        user_id=data["user_id"],
        people_id=data["people_id"]
    )
    
    db.session.add(new_favorite_people)
    db.session.commit()

    response_body = {
        "msg": f"El nuevo personaje favorito creado es: {new_favorite_people.people_id}",
        "new_favorite_people": new_favorite_people.serialize()
    }
    return jsonify(response_body), 201
#-------------------------------------GET-----ALL FAVORITE PEOPLE------------------------------------------------#

#https://redesigned-journey-pjp6gxqv494737x5w-3000.app.github.dev/favorite/people

@app.route('/favorite/people', methods=['GET'])
def get_favorite_people():
    list_favorite_people = Favorite_People.query.all()    
    obj_favorite_people = [favorite.serialize() for favorite in list_favorite_people]
    #print(obj_favorite_people)
    
    response_body = {
        "Favorite_people":obj_favorite_people
    }
    return jsonify(response_body), 200

#-------------------------------------DELETE-----FAVORITE PEOPLE------------------------------------------------#

@app.route('/favorite/people/<int:people_id>', methods = ['DELETE'])
def delete_favorite_people(people_id):

    user_id = 1
    exist = Favorite_People.query.filter_by(user_id = user_id, people_id=people_id).first()
    if exist :
        db.session.delete(exist)
        db.session.commit()
    return jsonify({"msg": "Personaje eliminado  de la tabla Favorite_People"})


#-------------------------------------DELETE-----FAVORITE PLANET------------------------------------------------#
#https://redesigned-journey-pjp6gxqv494737x5w-3000.app.github.dev/favorite/planet

@app.route('/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favorite_planet(planet_id):

    user_id = 1
    exist = Favorite_Planet.query.filter_by(user_id = user_id, planet_id=planet_id).first()
    if exist :
        db.session.delete(exist)
        db.session.commit()
    return jsonify({"msg": "Planeta eliminado  de la tabla Favorite_Planet"})

# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
