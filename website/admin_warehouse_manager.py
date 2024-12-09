from flask import Blueprint
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user
from .models import (Customer, Employee, Item, Service, SupplierItem, Supplier, Voucher, Warehouse, Zone,
                         PriceHistory, Product, ShippingStatus, OrderItem, Order, Rating, BrowsingHistory)
from flask import Flask, render_template
from flask_login import current_user

admin = Blueprint('admin_warehouse_manager', __name__)

@admin.route('/warehouse_manager')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')
