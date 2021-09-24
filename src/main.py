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
from models import db, User,Planet,Character,favorite_characters,favorite_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/create/user', methods=['GET'])
def list_of_user():
    user = User(
    password = "123",
    email = "prueba@prueba.com",
    is_active = True,
    characterfav = " ",
    planetfav = " ")
    db.session.add(user)
    
    user = User(
    password = "456",
    email = "otro@user.com",
    is_active = True,
    characterfav = " ",
    planetfav = " ")
    db.session.add(user)
    
    db.session.commit()

    return jsonify("it is ok"), 200

@app.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    users = list(map(lambda user : user.serialize(), users))
    return jsonify(users), 200

@app.route('/create/people', methods=['GET'])
def list_of_character():
    character = Character(
        name = "Luke Skywalker",
        height = "172",
        mass = "77",
        hair_color = "blond",
        homeworld = "Tatooine",
        eye_color = "blue",
        gender = "male"
        )
    db.session.add(character)

    character2 = Character(
        name = "Leia Organa",
        height = "150",
        mass = "49",
        hair_color = "brown",
        homeworld = "Alderaan",
        eye_color = "brown",
        gender = "female"
        )
    db.session.add(character2)
    
    db.session.commit()

    return jsonify("It is ok"), 200
    
@app.route('/people', methods=['GET'])
def get_character():
    characters = Character.query.all()
    characters = list(map(lambda character : character.serialize(), characters))
    return jsonify(characters), 200

@app.route('/create/planets', methods=['GET'])
def list_of_planet():
    planet = Planet(
    name = "Alderaan",
    diameter = "12500",
    population = "2000000000",
    climate = "temperate",
    terrain = "grasslands, mountains",
    surface_water = "40")
    db.session.add(planet)

    planet2 = Planet(
    name = "Tatooine",
    diameter = "10465",
    population = "200000",
    climate = "arid",
    terrain = "desert",
    surface_water = "1")
    db.session.add(planet2)
    
    db.session.commit()

    return jsonify("It is ok"), 200
    
@app.route('/planets', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    planets = list(map(lambda planet : planet.serialize(), planets))

    return jsonify(planets), 200
    
@app.route('/create/favorites', methods=['GET'])
def create_user_favorites():
    user = User.query.get(1)
    character = Character.query.filter_by(name = "Leia Organa").first()
    user.favorite_characters.append(character)
    db.session.add(user)
    db.session.commit()
    
    return jsonify("ok"), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    favorites = []
    for characterfav in user.favorite_characters:
        favorites.append(character.name)
        print(character.name)
    for planetfav in user.favorite_planets:
        favorites.append(planet.name)

    return jsonify(favorites), 200


@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_character(people_id):
    character = Character.query.get(people_id)
    return jsonify(character.serialize()), 200


@app.route("/planets/<int:planets_id>", methods=["GET"])
def get_one_planet(planets_id):
    planet = Planet.query.get(planets_id)
    return jsonify(planet.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
