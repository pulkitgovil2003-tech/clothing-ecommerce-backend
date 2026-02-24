from flask import Flask
from .config import Config
from .extensions import mongo, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.product_routes import product_bp
    from .routes.cart_routes import cart_bp
    from .routes.order_routes import order_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(order_bp, url_prefix="/api/orders")

    # Optional root route
    @app.route("/")
    def home():
        return "Clothing E-commerce Backend is running!"

    return app