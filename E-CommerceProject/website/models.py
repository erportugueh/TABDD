from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import (
    Document, EmbeddedDocument, fields, EmbeddedDocumentField, ListField, IntField, StringField, FloatField, DateTimeField, DynamicEmbeddedDocument
)
from datetime import datetime

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
    __tablename__ = 'EMPLOYEES'  # Match the table name in Oracle

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Identity column
    name = db.Column(db.String(25), nullable=False)  # Name column
    account_id = db.Column(db.String(20), nullable=False, unique=True)  # Account_ID column
    email = db.Column(db.String(35), nullable=False, unique=True)  # Email column
    password = db.Column(db.String(20), nullable=False)  # Password_Hash column
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
    __tablename__ = 'ITEMS'  # Oracle table name

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ITEM_ID
    name = db.Column(db.String(20), nullable=True)  # NAME
    description = db.Column(db.String(200), nullable=False)  # DESCRIPTION
    brand = db.Column(db.String(20), nullable=False)  # BRAND
    type = db.Column(db.String(20), nullable=False)  # TYPE
    primary_supplier_id = db.Column(db.Integer, nullable=False)  # PRIMARY_SUPPLIER_ID
    purchase_price = db.Column(db.Float, nullable=False)  # PURCHASE_PRICE
    sales_price = db.Column(db.Float, nullable=False)  # SALES_PRICE

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
class TechnicalInfo(DynamicEmbeddedDocument):
    # Allows arbitrary key-value pairs for technical attributes
    pass

class PhysicalInfo(DynamicEmbeddedDocument):
    # Allows arbitrary key-value pairs for physical attributes
    pass

class PriceHistory(EmbeddedDocument):
    Price = fields.FloatField(required=True)
    ChangedAt = fields.DateTimeField(required=True)
    Reason = fields.StringField()

class Product(Document):
    meta = {'collection': 'Products'}
    item_id = fields.IntField(required=True, unique=True)
    product_warehouse_id = fields.IntField(required=True)
    product_zone_id = fields.IntField(required=True)
    quantity_in_stock = fields.IntField(required=True)
    minimum_stock = fields.IntField(required=True)
    price = fields.FloatField(required=True)
    category = fields.StringField(required=True)
    subcategory = fields.StringField(required=True)
    discount = fields.FloatField(null=True)
    technical_info = fields.EmbeddedDocumentListField(TechnicalInfo)
    physical_info = fields.EmbeddedDocumentListField(PhysicalInfo)
    price_history = fields.EmbeddedDocumentListField(PriceHistory)
    image = fields.FileField()  # Stores binary image data
    Product_Aisle_ID = fields.IntField(required=True)

class ShippingStatus(EmbeddedDocument):
    Status = StringField(
        required=True,
        choices=['processing', 'preparing shipping', 'shipped', 'in transit', 'delivered'],
        description="Shipping status of the order."
    )
    Location = StringField(description="Current location of the shipment.")
    Timestamp = DateTimeField(required=True, description="Timestamp of the status update.")

class OrderItem(EmbeddedDocument):
    Order_Item_ID = IntField(description="Auto-generated Order Item ID.")
    Item_ID = IntField(required=True, description="Foreign key to the Item ID.")
    Quantity = IntField(required=True, description="Quantity of the item ordered.")
    Price = FloatField(required=True, description="Price of the item ordered.")

class Order(Document):
    meta = {'collection': 'Orders'}  # Specify the correct collection name
    Order_ID = IntField(primary_key=True, description="Auto-generated Order ID.")
    Customer_ID = IntField(required=True, description="Customer ID placing the order.")
    Delivery_Address = StringField(
        max_length=25, required=True, description="Delivery address for the order."
    )
    Payment_Status = StringField(required=True, description="Payment status of the order.")
    Checkout_Total = FloatField(required=True, description="Total checkout amount.")
    Discount = FloatField(description="Discount amount applied to the order.")
    Voucher_code = StringField(
        description="Voucher code applied to the order (nullable).", null=True
    )
    Purchase_date = DateTimeField(
        required=True, default=datetime.utcnow, description="Date the order was placed."
    )
    Delivery_date = DateTimeField(
        description="Date the order is delivered (nullable).", null=True
    )
    Time_preparation = IntField(description="Preparation time in minutes.")
    Shipping_Status = ListField(
        EmbeddedDocumentField(ShippingStatus),
        required=True,
        description="List of shipping status updates."
    )
    OrderItems = ListField(
        EmbeddedDocumentField(OrderItem),
        required=True,
        description="List of items in the order."

    )

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
