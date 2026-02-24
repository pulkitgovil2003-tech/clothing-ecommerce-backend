from app.extensions import mongo
from bson import ObjectId
from datetime import datetime

class OrderModel:

    @staticmethod
    def create_order(user_id, items):
        order = {
            "user_id": user_id,
            "items": items,
            "status": "Placed",
            "created_at": datetime.utcnow()
        }
        return mongo.db.orders.insert_one(order)

    @staticmethod
    def get_user_orders(user_id):
        orders = list(mongo.db.orders.find({"user_id": user_id}))
        for order in orders:
            order["_id"] = str(order["_id"])
        return orders

    @staticmethod
    def get_all_orders():
        orders = list(mongo.db.orders.find())
        for order in orders:
            order["_id"] = str(order["_id"])
        return orders