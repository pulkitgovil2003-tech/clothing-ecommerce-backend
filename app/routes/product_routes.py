from flask import Blueprint, request, jsonify
from app.extensions import mongo
from flask_jwt_extended import jwt_required

product_bp = Blueprint("products", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    products = list(mongo.db.products.find())
    for p in products:
        p["_id"] = str(p["_id"])
    return jsonify(products)


@product_bp.route("/", methods=["POST"])
@jwt_required()
def add_product():
    data = request.json

    mongo.db.products.insert_one({
        "name": data["name"],
        "price": data["price"],
        "category": data["category"],
        "stock": data["stock"]
    })

    return jsonify({"message": "Product added"}), 201