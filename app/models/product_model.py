from app.extensions import mongo
from bson import ObjectId

class ProductModel:

    @staticmethod
    def create_product(name, price, category, stock):
        product = {
            "name": name,
            "price": price,
            "category": category,
            "stock": stock
        }
        return mongo.db.products.insert_one(product)

    @staticmethod
    def get_all_products(filters=None):
        if filters is None:
            filters = {}

        products = list(mongo.db.products.find(filters))
        for p in products:
            p["_id"] = str(p["_id"])
        return products

    @staticmethod
    def get_product_by_id(product_id):
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
        return product

    @staticmethod
    def update_product(product_id, update_data):
        return mongo.db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete_product(product_id):
        return mongo.db.products.delete_one(
            {"_id": ObjectId(product_id)}
        )