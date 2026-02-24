from flask import Blueprint, request, jsonify, jwt_required, get_jwt_identity
from app.extensions import mongo, bcrypt
from flask_jwt_extended import create_access_token
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Name, email, and password are required"}), 400

    # Check if user exists
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    mongo.db.users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
        "role": "user"  # default role
    })

    return jsonify({"message": "User registered successfully"}), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    user = mongo.db.users.find_one({"email": data["email"]})

    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create JWT token including role
    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user["role"]}
    )

    return jsonify({"access_token": token})


user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()

    user = mongo.db.users.find_one(
        {"_id": ObjectId(current_user_id)},
        {"password": 0}   # exclude password
    )

    if not user:
        return jsonify({"message": "User not found"}), 404

    user["_id"] = str(user["_id"])

    return jsonify(user), 200