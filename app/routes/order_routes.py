from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import mongo
from datetime import datetime

order_bp = Blueprint("orders", __name__)

@order_bp.route("/place", methods=["POST"])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    item_name = data.get("item_name")  # optional

    if item_name:
        cart_items = list(mongo.db.carts.find({
            "user_id": user_id,
            "product_name": item_name
        }))
    else:
        cart_items = list(mongo.db.carts.find({"user_id": user_id}))

    if not cart_items:
        return jsonify({"message": "No matching items found in cart"}), 400

    order_items = []
    total_amount = 0

    for item in cart_items:
        product_total = item["price"] * item["quantity"]
        total_amount += product_total

        order_items.append({
            "product_name": item["product_name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "total": product_total
        })

    order_data = {
        "user_id": user_id,
        "items": order_items,
        "total_amount": total_amount,
        "status": "Placed",
        "created_at": datetime.utcnow()
    }

    mongo.db.orders.insert_one(order_data)

    # Delete only selected items
    if item_name:
        mongo.db.carts.delete_many({
            "user_id": user_id,
            "product_name": item_name
        })
    else:
        mongo.db.carts.delete_many({"user_id": user_id})

    return jsonify({
        "message": "Order placed successfully",
        "total_amount": total_amount
    }), 201


@order_bp.route("/my-orders", methods=["GET"])
@jwt_required()
def get_my_orders():
    user_id = get_jwt_identity()

    orders = list(mongo.db.orders.find({"user_id": user_id}))

    for order in orders:
        order["_id"] = str(order["_id"])
        order["created_at"] = order["created_at"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "total_orders": len(orders),
        "orders": orders
    }), 200