from . import db
import random
from datetime import datetime  # For default timestamps and date handling

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint

# MongoEngine for MongoDB Models
from mongoengine import Document, EmbeddedDocument, fields

# Oracle Tables
class Customer(db.Model, UserMixin):
    __tablename__ = 'CUSTOMERS'  # Oracle table name

    customer_id = db.Column(db.Integer, primary_key=True)  # CUSTOMER_ID
    name = db.Column(db.String(25), nullable=True)  # NAME
    address = db.Column(db.String(50), nullable=False)  # ADDRESS
    postal_code = db.Column(db.String(15), nullable=False)  # POSTAL_CODE
    nif = db.Column(db.String(15), nullable=False)  # NIF
    email = db.Column(db.String(35), nullable=False, unique=True)  # EMAIL
    account_id = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)  # PASSWORD_HASH
    gdpr_terms = db.Column(db.Text, nullable=False)  # GDPR_TERMS (CLOB)
    accepted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # ACCEPTED_DATE
    points_balance = db.Column(db.Integer, nullable=True, default=0)  # POINTS_BALANCE
    last_points_redeemed_date = db.Column(db.DateTime, nullable=True)  # LAST_POINTS_REDEEMED_DATE
    status = db.Column(db.String(10), nullable=False)  # STATUS

    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def get_id(self):
        return str(self.customer_id)  # Returns the customer_id as a string

    def __str__(self):
        return '<Customer %r>' % Customer.id

class Employee(db.Model):
    __tablename__ = 'Employees'  # Match the table name in Oracle

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Identity column
    name = db.Column(db.String(25), nullable=False)  # Name column
    account_id = db.Column(db.String(20), nullable=False, unique=True)  # Account_ID column
    email = db.Column(db.String(35), nullable=False, unique=True)  # Email column
    password_hash = db.Column(db.String(20), nullable=False)  # Password_Hash column
    role = db.Column(db.String(15), nullable=False)  # Role column

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Employee(name={self.name}, email={self.email}, role={self.role})>"

class Item(db.Model):
    __tablename__ = 'Items'  # Oracle table name

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ITEM_ID
    name = db.Column(db.String(20), nullable=True)  # NAME
    description = db.Column(db.String(50), nullable=False)  # DESCRIPTION
    brand = db.Column(db.String(20), nullable=False)  # BRAND
    type = db.Column(db.String(20), nullable=False)  # TYPE
    primary_supplier_id = db.Column(db.Integer, nullable=False)  # PRIMARY_SUPPLIER_ID
    purchase_price = db.Column(db.Float, nullable=False)  # PURCHASE_PRICE
    sales_price = db.Column(db.Float, nullable=False)  # SALES_PRICE

    # Add validation for 'Type' column
    __table_args__ = (
        db.CheckConstraint("Type IN ('Service', 'Product')", name='check_type_valid'),
    )

    def __repr__(self):
        return (f"<Item(name={self.name}, brand={self.brand}, type={self.type}, "
                f"purchase_price={self.purchase_price}, sales_price={self.sales_price})>")

class Service(db.Model):
    __tablename__ = 'Services'  # Oracle table name

    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # SERVICE_ID
    max_execution_hours = db.Column(db.Float, nullable=False)  # MAX_EXECUTION_HOURS
    execution_time = db.Column(db.Float, nullable=False)  # EXECUTION_TIME
    responsible_employee_id = db.Column(db.Integer, nullable=False)  # RESPONSIBLE_EMPLOYEE_ID
    price = db.Column(db.Float, nullable=False)  # PRICE

    def __repr__(self):
        return (f"<Service(service_id={self.service_id}, max_execution_hours={self.max_execution_hours}, "
                f"execution_time={self.execution_time}, responsible_employee_id={self.responsible_employee_id}, "
                f"price={self.price})>")

class Supplier(db.Model):
    __tablename__ = 'Suppliers'  # Oracle table name

    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # SUPPLIER_ID
    name = db.Column(db.String(20), nullable=True)  # NAME
    contact_info = db.Column(db.String(20), nullable=False)  # CONTACT_INFO
    best_selling_item_id = db.Column(db.Integer, nullable=True)  # BEST_SELLING_ITEM_ID

    def __repr__(self):
        return (f"<Supplier(supplier_id={self.supplier_id}, name={self.name}, "
                f"contact_info={self.contact_info}, best_selling_item_id={self.best_selling_item_id})>")

class SupplierItem(db.Model):
    __tablename__ = 'SupplierItems'  # Oracle table name

    supplier_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # SUPPLIER_ITEM_ID
    supplier_id = db.Column(db.Integer, nullable=False)  # SUPPLIER_ID
    item_id = db.Column(db.Integer, nullable=False)  # ITEM_ID
    price = db.Column(db.Float, nullable=False)  # PRICE
    availability = db.Column(db.String(10), nullable=False)  # AVAILABILITY

    def __repr__(self):
        return (f"<SupplierItem(supplier_item_id={self.supplier_item_id}, supplier_id={self.supplier_id}, "
                f"item_id={self.item_id}, price={self.price}, availability={self.availability})>")

class Voucher(db.Model):
    __tablename__ = 'VOUCHERS'  # Matches the Oracle table name

    voucher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # VOUCHER_ID
    customer_id = db.Column(db.Integer, nullable=False)  # CUSTOMER_ID
    voucher_code = db.Column(db.String(50), nullable=False, unique=True)  # VOUCHER_CODE
    amount = db.Column(db.Float, nullable=False)  # AMOUNT
    valid_until = db.Column(db.Date, nullable=False)  # VALID_UNTIL

    def __repr__(self):
        return (f"<Voucher(voucher_id={self.voucher_id}, customer_id={self.customer_id}, "
                f"voucher_code='{self.voucher_code}', amount={self.amount}, valid_until={self.valid_until})>")

class Warehouse(db.Model):
    __tablename__ = 'Warehouses'  # Oracle table name

    warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # WAREHOUSE_ID
    name = db.Column(db.String(15), nullable=False, unique=True)  # NAME
    address = db.Column(db.String(50), nullable=False)  # ADDRESS
    location = db.Column(db.String(10), nullable=False)  # LOCATION

    def __repr__(self):
        return (f"<Warehouse(warehouse_id={self.warehouse_id}, name={self.name}, "
                f"address={self.address}, location={self.location})>")

class Zone(db.Model):
    __tablename__ = 'Zones'  # Oracle table name

    zone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ZONE_ID
    capacity = db.Column(db.Float, nullable=False)  # CAPACITY
    warehouse_id = db.Column(db.Integer, nullable=False)  # WAREHOUSE_ID

    def __repr__(self):
        return (f"<Zone(zone_id={self.zone_id}, capacity={self.capacity}, "
                f"warehouse_id={self.warehouse_id})>")

# MongoDB Tables
class PriceHistory(EmbeddedDocument):
    """
    Embedded document to store the history of price changes.
    """
    price = fields.FloatField(required=True, db_field='Price')  # Map to MongoDB schema
    changed_at = fields.DateTimeField(required=True, db_field='ChangedAt')  # Map to MongoDB schema
    reason = fields.StringField(db_field='Reason')  # Map to MongoDB schema

class Product(Document):
    """
    MongoDB collection model for Products.
    """
    meta = {'collection': 'Products'}  # The name of your MongoDB collection

    _id = fields.IntField(required=True, primary_key=True)
    item_id = fields.IntField(required=True, db_field='Item_ID')  # Map to MongoDB schema
    product_warehouse_id = fields.IntField(required=True, db_field='Product_Warehouse_ID')  # Map to MongoDB schema
    product_zone_id = fields.IntField(required=True, db_field='Product_Zone_ID')  # Map to MongoDB schema
    quantity_in_stock = fields.IntField(required=True, db_field='Quantity_in_Stock')  # Map to MongoDB schema
    minimum_stock = fields.IntField(required=True, db_field='Minimum_Stock')  # Map to MongoDB schema
    price = fields.FloatField(required=True, db_field='Price')  # Map to MongoDB schema
    category = fields.StringField(required=True, db_field='Category')  # Map to MongoDB schema
    subcategory = fields.StringField(required=True, db_field='Subcategory')  # Map to MongoDB schema
    discount = fields.FloatField(db_field='Discount', null=True)  # Map to MongoDB schema
    price_history = fields.EmbeddedDocumentListField(PriceHistory, db_field='PriceHistory')  # Map to MongoDB schema

class ShippingStatus(EmbeddedDocument):
    """
    Embedded document to track shipping status changes over time.
    """
    status = fields.StringField(
        required=True,
        choices=["processing", "reparing shipping", "shipped", "in transit", "delivered"]
    )
    location = fields.StringField()  # Location is optional
    timestamp = fields.DateTimeField(required=True, default=datetime.utcnow)

class OrderItem(EmbeddedDocument):
    """
    Embedded document to store items in an order.
    """
    order_item_id = fields.IntField()  # Auto-generated, not required explicitly
    fk_item_id = fields.IntField(required=True)
    fk_order_id = fields.IntField()  # Matches Order_ID, optional for MongoDB
    quantity = fields.IntField(required=True)
    price = fields.FloatField(required=True)

class Order(Document):
    """
    MongoDB collection model for Orders.
    """
    meta = {'collection': 'Orders'}  # MongoDB collection name

    # Fields as per schema
    order_id = fields.IntField(required=False)  # Auto-generated
    customer_id = fields.IntField(required=True)
    delivery_address = fields.StringField(max_length=25, required=True)
    payment_status = fields.StringField(required=True)
    checkout_total = fields.FloatField(required=True)
    shipping_status = fields.EmbeddedDocumentListField(ShippingStatus, required=True)  # Array of statuses
    order_items = fields.EmbeddedDocumentListField(OrderItem, required=True)  # Array of items

class Rating(Document):
    """
    MongoDB collection model for Ratings.
    """
    meta = {'collection': 'Ratings'}  # MongoDB collection name

    # Fields as per schema
    customer_id = fields.IntField(required=True)  # Client ID
    item_id = fields.IntField(required=True)  # Item ID
    rating = fields.IntField(required=True, min_value=1, max_value=5)  # Rating from 1 to 5
    comment = fields.StringField()  # Optional client comment

    def __repr__(self):
        return (f"<Rating(customer_id={self.customer_id}, item_id={self.item_id}, "
                f"rating={self.rating}, comment={self.comment})>")

class BrowsingHistory(Document):
    """
    MongoDB collection model for Browsing History.
    """
    meta = {'collection': 'BrowsingHistory'}  # MongoDB collection name

    # Fields as per schema
    customer_id = fields.IntField(required=True)  # Client ID
    page = fields.StringField(required=True)  # Accessed page URL
    visit_date_time = fields.DateTimeField(required=True)  # Visit date/time in ISODate format

    def __repr__(self):
        return (f"<BrowsingHistory(customer_id={self.customer_id}, page={self.page}, "
                f"visit_date_time={self.visit_date_time})>")

class CartItem(EmbeddedDocument):
    item_id = fields.IntField(required=True)
    item_name = fields.StringField(required=True)
    price = fields.FloatField(required=True, min_value=0)
    discount = fields.FloatField(required=True, min_value=0, max_value=1)
    quantity = fields.IntField(required=True, min_value=1)

class Cart(Document):
    meta = {'collection': 'Carts'}
    customer_id = fields.IntField(required=True, unique=True, db_field="Customer_ID")
    items = fields.EmbeddedDocumentListField(CartItem, db_field="Items")
