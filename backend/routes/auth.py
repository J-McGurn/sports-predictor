from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from models import db
from models.user import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {
            "error": "Username, email and password are required"
        }, 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return {
            "error": "Username or email already exists"
        }, 409

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully",
        "username": user.username
    }, 201
    
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "error": "Email and password are required"
        }, 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return {
            "error": "Invalid email or password"
        }, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "access_token": access_token,
        "username": user.username
    }, 200
    
@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return {
            "error": "User not found"
        }, 404

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }, 200