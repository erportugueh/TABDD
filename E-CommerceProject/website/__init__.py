from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from mongoengine import connect
from flask_login import LoginManager
from flask_login import current_user
import os

db = SQLAlchemy()

# Oracle Connection
oracle_username = "C##e_commerce"
oracle_password = "qKCH1brdHfWtMFadWdbzWeMJS3rHDJ"
oracle_host = "vsgate-s1.dei.isep.ipp.pt"
oracle_port = 10434
oracle_service = "xe"

# MongoDB Connection
username = "ecommerce_user"
password = "secure_password"
host = "vsgate-s1.dei.isep.ipp.pt"
port = 10911
db_name = "EcommerceDB"

def create_app():
    app = Flask(__name__)
    # Set a secret key (you can use a secure random key)
    app.config['SECRET_KEY'] = os.urandom(24)
    # Oracle database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'oracle+cx_oracle://C##e_commerce:qKCH1brdHfWtMFadWdbzWeMJS3rHDJ@'
        f'vsgate-s1.dei.isep.ipp.pt:10434/xe'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(email):
        from .models import Customer, Employee
        # Type checks
        if isinstance(email, int):
            user = Customer.query.get(email)
        elif isinstance(email, str):
            user = Employee.query.filter_by(email=email).first()

        return user

    from .views import views
    from .auth import auth
    from .admin import admin
    from .cart import cart_bp
    from .customer import customer

    from .models import (Customer, Employee, Item, Service, SupplierItem, Supplier, Voucher, Warehouse, Zone,
                         PriceHistory, Product, ShippingStatus, OrderItem, Order, Rating, BrowsingHistory)

    app.register_blueprint(views, url_prefix='/') #localhost:5000/orders or cart or about-us
    app.register_blueprint(auth, url_prefix='/') #localhost:5000/auth/login or register or change password
    app.register_blueprint(admin, url_prefix='/')  # localhost:5000
    app.register_blueprint(cart_bp, url_prefix='/') #localhost:5000
    app.register_blueprint(customer, url_prefix='/')  # localhost:5000

    # Test Oracle connection
    try:
        with app.app_context():
            result = db.session.execute(text('SELECT 1 FROM DUAL'))  # Test query
            print("Oracle connection successful.")
    except Exception as e:
        print(f"Oracle connection failed: {e}")

    # Test MongoDB Connection
    try:
        mongo_connection = connect(
            db=db_name,
            username=username,
            password=password,
            host=f"mongodb://{host}:{port}/{db_name}"
        )
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

    return app