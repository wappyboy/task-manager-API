from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 409
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200
