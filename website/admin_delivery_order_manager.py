<<<<<<< Updated upstream
from flask import Blueprint

admin = Blueprint('admin_delivery_order_manager', __name__)
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




@admin.route('/order_location', methods=['GET', 'POST'])
@login_required
def display_order_location():
    if current_user.id == 2:
        if request.method == 'POST':
            date = request.form.get('date')
            time = request.form.get('time')
            # Call the function to get order locations
            orders = order_location_at_datetime(date, time)
            if orders:
                return render_template('order_location.html', orders=orders, date=date, time=time)
            else:
                return f"No orders found on {date} at {time}."

        return render_template('order_location_form.html')

    return render_template('404.html')



@admin.route('/order_route', methods=['GET', 'POST'])
@login_required
def display_order_route():
    if current_user.id == 2:
        if request.method == 'POST':
            order_id = request.form.get('order_id')
            order_info = get_order_route(order_id)
            if order_info:
                return render_template('order_route.html', order=order_info)
            else:
                return f"No route information found for Order ID: {order_id}."

        return render_template('order_route_form.html')

    return render_template('404.html')

#US11
def order_location_at_datetime(date, time):
    # Query MongoDB to find orders matching the specified date and time
    location_at_datetime = db.orders.find({
        "OrderDate": date,
        "OrderTime": time
    }, {
        "Customer_ID": 1,
        "OrderDate": 1,
        "OrderTime": 1,
        "Current_Location": 1
    })

    # Collect results in a list
    orders_info = []
    for order in location_at_datetime:
        orders_info.append({
            "order_id": str(order['_id']),
            "customer_id": order['Customer_ID'],
            "order_date": order['OrderDate'],
            "order_time": order['OrderTime'],
            "current_location": order['Current_Location']
        })

    return orders_info

#US12
def get_order_route(order_id):
    try:
        # Query MongoDB to find the order by its ID
        order = db.orders.find_one({
            "_id": ObjectId(order_id)
        }, {
            "Customer_ID": 1,
            "route": 1
        })

        if order:
            return {
                "order_id": str(order['_id']),
                "customer_id": order['Customer_ID'],
                "route": order.get('route', 'Route not available')
            }
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
>>>>>>> Stashed changes
