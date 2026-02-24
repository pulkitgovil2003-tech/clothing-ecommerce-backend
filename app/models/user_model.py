from app.extensions import mongo
from bson import ObjectId

class UserModel:

    @staticmethod
    def create_user(name, email, password, role="user"):
        user = {
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }
        return mongo.db.users.insert_one(user)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})