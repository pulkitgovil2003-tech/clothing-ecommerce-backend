from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import mongo

order_bp = Blueprint("orders", __name__)

@order_bp.route("/place", methods=["POST"])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()

    cart_items = list(mongo.db.carts.find({"user_id": user_id}))

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    mongo.db.orders.insert_one({
        "user_id": user_id,
        "items": cart_items,
        "status": "Placed"
    })

    mongo.db.carts.delete_many({"user_id": user_id})

    return jsonify({"message": "Order placed successfully"})