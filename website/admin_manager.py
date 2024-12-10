<<<<<<< Updated upstream
from flask import Blueprint

admin = Blueprint('admin_manager', __name__)
=======
from flask import Blueprint, request
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user
from .models import (Customer, Employee, Item, Service, SupplierItem, Supplier, Voucher, Warehouse, Zone,
                     PriceHistory, Product, ShippingStatus, OrderItem, Order, Rating, BrowsingHistory)
from flask import Flask, render_template
from flask_login import current_user
from bson.objectid import ObjectId

admin = Blueprint('admin_warehouse_manager', __name__)

from pymongo import MongoClient
from sqlalchemy import create_engine, text

# Initialize MongoDB Client

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['your_mongo_db']

# Initialize SQLAlchemy Engine for Oracle
engine = create_engine('oracle+cx_oracle://username:password@host:port/service_name')


@admin.route('/top_voucher_customer_products')
@login_required
def display_top_voucher_customer_products():
    if current_user.id == 2:

        products = get_products_by_top_voucher_customer()
        if products:
            return render_template('top_voucher_customer_products.html', products=products)
        else:
            # If there are no products or no customer found
            return render_template('404.html', message="No customer found who used vouchers or no products.")
    return render_template('404.html')


def get_products_by_top_voucher_customer():
    pipeline_US13 = [
        {"$group": {
            "_id": "$CustomerID",  # Group by CustomerID
            "total_count_vouchers": {"$sum": 1}  # Count the number of orders (vouchers)
        }},
        {"$sort": {"total_count_vouchers": -1}},  # Sort by total vouchers used (descending)
        {"$limit": 1}  # Get the customer with the highest number of vouchers
    ]

    top_voucher_customer = list(db.Orders.aggregate(pipeline_US13))

    if top_voucher_customer:
        # Get the customer ID of the top voucher user
        customer_id = top_voucher_customer[0]['_id']

        # Find the products purchased by this customer (OrderItems)
        products_purchase = db.orders.find_one({"Customer_ID": customer_id}, {"OrderItems": 1, "_id": 0})

        if products_purchase:
            # Initialize a list to store product details
            product_details = []

            # Loop through the 'OrderItems' and collect product info
            for item in products_purchase['OrderItems']:
                product_details.append({
                    "Product ID": item['FK_Item_ID'],
                    "Quantity": item['Quantity'],
                    "Price": item['Price']
                })

            return product_details  # Return the list of products purchased
        else:
            return "No products found for this customer."
    else:
        return "No customer found who used vouchers."
>>>>>>> Stashed changes
