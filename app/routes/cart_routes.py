from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import mongo
from bson import ObjectId

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.json

    mongo.db.carts.insert_one({
        "user_id": user_id,
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    })

    return jsonify({"message": "Added to cart"})

@cart_bp.route("/", methods=["GET"])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()

    cart_items = mongo.db.carts.find({"user_id": user_id})

    result = []

    for item in cart_items:
        product = mongo.db.products.find_one(
            {"_id": ObjectId(item["product_id"])}
        )

        result.append({
            "cart_id": str(item["_id"]),
            "product_id": str(item["product_id"]),
            "product_name": product["name"] if product else "Product Deleted",
            "price": product["price"] if product else 0,
            "quantity": item["quantity"],
            "total_price": (product["price"] * item["quantity"]) if product else 0
        })

    return jsonify({
        "message": "Cart fetched successfully",
        "items": result
    }), 200