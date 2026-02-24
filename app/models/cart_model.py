from app.extensions import mongo
from bson import ObjectId

class CartModel:

    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        cart_item = {
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity
        }
        return mongo.db.carts.insert_one(cart_item)

    @staticmethod
    def get_user_cart(user_id):
        items = list(mongo.db.carts.find({"user_id": user_id}))
        for item in items:
            item["_id"] = str(item["_id"])
        return items

    @staticmethod
    def clear_cart(user_id):
        return mongo.db.carts.delete_many({"user_id": user_id})