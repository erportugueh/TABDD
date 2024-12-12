<<<<<<< Updated upstream
from flask import Blueprint
from flask import Blueprint
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user
from .models import (Customer, Employee, Item, Service, SupplierItem, Supplier, Voucher, Warehouse, Zone,
                         PriceHistory, Product, ShippingStatus, OrderItem, Order, Rating, BrowsingHistory)
from flask import Flask, render_template
from flask_login import current_user

admin = Blueprint('admin', __name__)

@admin.route('/manager')
@login_required
def display_customers():

        return
=======
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/cio')
@login_required
def cio():
    return render_template('adminCIO.html')

@admin.route('/deliveryOrderManager')
@login_required
def delivery_order_manager():
    return render_template('adminDeliveryOrderManager.html')

@admin.route('/warehouseManager')
@login_required
def warehouse_anager():
    return render_template('adminWarehouseManager.html')

@admin.route('/manager')
@login_required
def manager():
    return render_template('adminManager.html')

@admin.route('/profileEmployee/<int:employee_id>')
@login_required
def profile_employee_view(employee_id):

    return render_template('employeeDetails.html')
>>>>>>> Stashed changes
