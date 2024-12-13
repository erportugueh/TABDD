from flask import Flask, render_template  # Import Flask framework and template rendering function
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM and database interaction
from sqlalchemy.sql import text  # Import raw SQL execution utility
from mongoengine import connect  # Import MongoDB connection library
from flask_login import LoginManager  # Import Flask-Login for user session management
import os  # Import OS module for environment and file operations

db = SQLAlchemy()  # Initialize the SQLAlchemy instance

# Oracle Connection
oracle_username = "C##e_commerce"  # Oracle database username
oracle_password = "qKCH1brdHfWtMFadWdbzWeMJS3rHDJ"  # Oracle database password
oracle_host = "vsgate-s1.dei.isep.ipp.pt"  # Oracle database host address
oracle_port = 10434  # Oracle database port
oracle_service = "xe"  # Oracle database service name

# MongoDB Connection
username = "ecommerce_user"  # MongoDB username
password = "secure_password"  # MongoDB password
host = "vsgate-s1.dei.isep.ipp.pt"  # MongoDB host address
port = 10911  # MongoDB port
db_name = "EcommerceDB"  # MongoDB database name

def create_app():
    app = Flask(__name__)  # Create Flask app instance
    # Set a secret key (for session security)
    app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key
    # Oracle database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'oracle+cx_oracle://{oracle_username}:{oracle_password}@{oracle_host}:{oracle_port}/{oracle_service}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

    db.init_app(app)  # Initialize SQLAlchemy with the Flask app

    @app.errorhandler(404)
    def page_not_found(error):  # Define custom handler for 404 errors
        return render_template('404.html')  # Render custom 404 error page

    login_manager = LoginManager()  # Initialize the LoginManager
    login_manager.init_app(app)  # Attach LoginManager to the Flask app
    login_manager.login_view = 'auth.login'  # Set default login view

    @login_manager.user_loader
    def load_user(email):  # Define user loading function for login management
        from .models import Customer, Employee  # Import models for user data retrieval
        # Type checks for determining whether the email is an integer or string
        if isinstance(email, int):
            user = Customer.query.get(email)  # Fetch customer by ID
        elif isinstance(email, str):
            user = Employee.query.filter_by(email=email).first()  # Fetch employee by email
        return user

    # Import blueprints for different app components
    from .views import views
    from .auth import auth
    from .admin import admin
    from .cart import cart_bp
    from .customer import customer

    # Import all models used in the app for database management
    from .models import (Customer, Employee, Item, Service, SupplierItem, Supplier, Voucher, Warehouse, Zone,
                         PriceHistory, Product, ShippingStatus, OrderItem, Order, Rating, BrowsingHistory)

    # Register blueprints to structure app routes
    app.register_blueprint(views, url_prefix='/')  # Main views
    app.register_blueprint(auth, url_prefix='/')  # Authentication-related routes
    app.register_blueprint(admin, url_prefix='/')  # Admin-related routes
    app.register_blueprint(cart_bp, url_prefix='/')  # Cart-related routes
    app.register_blueprint(customer, url_prefix='/')  # Customer-related routes

    # Test Oracle connection
    try:
        with app.app_context():
            result = db.session.execute(text('SELECT 1 FROM DUAL'))  # Test query for Oracle
            print("Oracle connection successful.")  # Connection success message
    except Exception as e:
        print(f"Oracle connection failed: {e}")  # Connection failure message

    # Test MongoDB Connection
    try:
        mongo_connection = connect(
            db=db_name,
            username=username,
            password=password,
            host=f"mongodb://{host}:{port}/{db_name}"  # MongoDB connection string
        )
        print("MongoDB connection successful.")  # Connection success message
    except Exception as e:
        print(f"MongoDB connection failed: {e}")  # Connection failure message

    return app  # Return the Flask app instance
