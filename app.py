import os
import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, create_access_token, jwt_required
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
Migrate(app, db) # flask db init, flask db migrate, flask db upgrade
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def main():
    return jsonify({"message": "API REST con JWT"})


@app.route('/api/register', methods=['POST'])
def register():
    
    correoelectronico= request.json.get("correoelectronico")
    password = request.json.get("password")
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    direccion = request.json.get("direccion")
    pais = request.json.get("pais")
    region = request.json.get("region")
    fechanac = request.json.get("fechanac")
    
    # Validamos los datos ingresados
    if not correoelectronico:
        return jsonify({"fail": "correo electrónico es requerido!"}), 422
    
    if not password:
        return jsonify({"fail": "password es requerido!"}), 422

    if not nombre:
        return jsonify({"fail": "nombre es requerido"}), 422

    if not apellido:
        return jsonify({"fail": "apellido es requerido"}), 422

    if not direccion:
        return jsonify({""}), 

    if not pais:
        return jsonify({"fail": "pais es requerido"}), 422

    if not region:
        return jsonify({"fail": "region es requerida"}), 422

    if not fechanac:
        return jsonify({"fail": "fechanac es requerids"}), 422


    # Buscamos el usuario a ver si ya existe con ese username
    userFound = User.query.filter_by(correoelectronico=correoelectronico).first()
    
    if userFound:
        return jsonify({"fail": "correo electrónico ya está en uso!"}), 400
    
    # Aqui estamos creando al nuevo usuario
    user = User()
    user.correoelectronico = correoelectronico
    user.password = generate_password_hash(password) 
    user.save()
    
    return jsonify({ "success": "Registro exitoso, por favor inicie sesion!"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    correoelectronico = request.json.get("correoelectronico")
    password = request.json.get("password")
    
    # Validamos los datos ingresados
    if not username:
        return jsonify({"fail": "correoelectronico es requerido!"}), 422
    
    if not password:
        return jsonify({"fail": "password es requerido!"}), 422
    
    # buscamos al usuario 
    user = User.query.filter_by(correoelectronico=correoelectronico).first()
    
    # si no exite el usuario 
    if not user:
        return jsonify({ "fail": "correo electrónico o password son incorrectos!"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({ "fail": "correo electrónico o password son incorrectos!"}), 401
    
    # expires = datetime.timedelta(days=5)
    # access_token = create_access_token(identity=user.id, expires_delta=expires)
    access_token = create_access_token(identity=user.id)
    
    data = {
        "success": "Inicio de sesion exitoso!",
        "access_token": access_token,
        "type": "Bearer",
        "user": user.serialize()
    }
    
    return jsonify(data), 200

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    user = User.query.get(id)
    
    return jsonify({ "message": "Ruta privada", "user": user.correoelectronico }), 200


if __name__ == '__main__':
    app.run()