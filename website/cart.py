from flask import Blueprint, request, jsonify, render_template, flash, redirect
from flask_login import current_user, login_required
from .models import Cart, CartItem, Voucher
import random
from sqlalchemy.sql import text
from . import db
from datetime import datetime

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/view', methods=['GET', 'POST'])
@login_required
def view_cart():
    # Fetch the cart for the current user
    cart = Cart.objects(customer_id=current_user.customer_id).first()
    if not cart:
        return render_template('checkout.html', cart=None, totals=None, result=None), 200

    # Calculate initial totals
    totals = calculate_totals(cart)

    # Check if a voucher code is submitted
    if request.method == 'POST':
        results = apply_voucher(cart, totals)
    else:
        # No voucher applied yet, show the default total
        results = {
            "totals": totals,
            "message": "No voucher code provided.",
            "success": False
        }

    # Render the page with the cart, totals, and result
    return render_template('checkout.html', cart=cart, results=results), 200


def calculate_totals(cart):
    total_price = sum((item.price - item.price * item.discount) * item.quantity for item in cart.items)
    taxes = 0.23 * total_price  # Fixed tax rate
    shipping_cost = sum(random.uniform(1.0, 5.0) for _ in cart.items)
    total_price_with_taxes_and_shipping = total_price + taxes + shipping_cost
    return {
        "total_price": total_price,
        "taxes": taxes,
        "shipping_cost": shipping_cost,
        "final_total": total_price_with_taxes_and_shipping,
        "final_total_discounted": total_price_with_taxes_and_shipping,
        "voucher_code": ''
    }


def apply_voucher(cart, totals):
    # Get the voucher code from the form submission
    voucher_code = request.form.get('voucher_code')

    voucher = Voucher.query.filter_by(
        customer_id=cart.customer_id,
        voucher_code=voucher_code
    ).first()

    print()
    if voucher:
        print("Voucher found")
        totals["final_total_discounted"] = max(totals["final_total"] - voucher.amount, 0)  # Ensure non-negative total
        totals["voucher_code"] = voucher_code
        return {
            "totals": totals,
            "message": "Voucher applied successfully!",
            "success": True
        }
    else:
        print("Voucher invalid")
        # Invalid or expired voucher
        totals["final_total_discounted"] = totals["final_total"]  # No discount applied
        return {
            "totals": totals,
            "message": "Invalid or expired voucher.",
            "success": False
        }

@cart_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    customer_id = data.get('customer_id')
    product = data.get('product')

    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id, items=[], total_price=0.0)

    # Check if item already in cart
    for item in cart.items:
        if item.product_id == product['product_id']:
            item.quantity += 1
            cart.total_price += item.price
            break
    else:
        new_item = CartItem(**product)
        cart.items.append(new_item)
        cart.total_price += new_item.price

    cart.save()
    return jsonify({"message": "Item added to cart"}), 200


@cart_bp.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.json
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')

    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    for item in cart.items:
        if item.product_id == product_id:
            cart.total_price -= item.price * item.quantity
            cart.items.remove(item)
            break

    cart.save()
    return jsonify({"message": "Item removed from cart"}), 200


@cart_bp.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    customer_id = request.json.get('customer_id')
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    cart.items = []
    cart.total_price = 0.0
    cart.save()
    return jsonify({"message": "Cart cleared"}), 200
