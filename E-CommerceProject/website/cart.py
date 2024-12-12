from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Cart, CartItem, Voucher, Product, Order, OrderItem
import random
from datetime import datetime, timedelta
from mongoengine import DoesNotExist
from .views import get_product
from sqlalchemy import text
from . import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/checkout', methods=['GET', 'POST'])
@login_required
def checkout_cart():
    # Fetch the cart for the current user
    cart = Cart.objects(customer_id=current_user.customer_id).first()
    if not cart:
        return render_template('cart.html', cart=None, totals=None, result=None), 200

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

@cart_bp.route('/cart/cart_view', methods=['GET', 'POST'])
@login_required
def view_cart():
    # Fetch the cart for the current user
    cart = Cart.objects(customer_id=current_user.customer_id).first()
    if not cart:
        return render_template('cart.html', cart=None), 200

    total=sum((item.price - item.price * item.discount) * item.quantity for item in cart.items)

    for item in cart.items:
        item.product = get_product(item.item_id)

    # Render the page with the cart, totals, and result
    return render_template('cart.html', cart=cart, total=total), 200

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
    customer_id = request.form.get('customer_id')
    item_id = int(request.form.get('item_id'))

    # Add the item to the cart
    result = add_item(customer_id, item_id)

    # Fetch the updated cart to calculate the new total
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        flash("Cart not found", "danger")
        return redirect('/cart/view')

    for item in cart.items:
        item.product = get_product(item.item_id)

    # Calculate the new total
    total = sum((item.price - item.price * item.discount) * item.quantity for item in cart.items)

    # Render the cart view with the updated total
    return render_template('cart.html', cart=cart, total=total, message=result["message"])

@cart_bp.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    customer_id = request.form.get('customer_id')
    item_id = int(request.form.get('item_id'))

    # Remove the item or decrease its quantity
    result = remove_item(customer_id, item_id)

    # Fetch the updated cart to calculate the new total
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        flash("Cart not found", "danger")
        return redirect('/cart/view')

    for item in cart.items:
        item.product = get_product(item.item_id)

    # Calculate the new total
    total = sum((item.price - item.price * item.discount) * item.quantity for item in cart.items)

    # Render the cart view with the updated total
    return render_template('cart.html', cart=cart, total=total, message=result["message"])

@cart_bp.route('/cart/clear-item', methods=['POST'])
@login_required
def clear_from_cart():
    customer_id = request.form.get('customer_id')
    item_id = int(request.form.get('item_id'))

    # Remove the item completely from the cart
    result = clear_item(customer_id, item_id)

    # Fetch the updated cart to calculate the new total
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        flash("Cart not found", "danger")
        return redirect('/cart/view')

    for item in cart.items:
        item.product = get_product(item.item_id)

    # Calculate the new total
    total = sum((item.price - item.price * item.discount) * item.quantity for item in cart.items)

    # Render the cart view with the updated total
    return render_template('cart.html', cart=cart, total=total, message=result["message"])

def add_item(customer_id, item_id):
    # Fetch the customer's cart
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id, items=[])

    # Check if the item already exists in the cart
    for item in cart.items:
        if item.item_id == item_id:
            item.quantity += 1
            cart.save()
            return {"message": "Item quantity increased", "success": True}

    # If item does not exist, fetch product details
    try:
        product = Product.objects.get(item_id=item_id)  # Adjust for your Product model and field names
    except DoesNotExist:
        return {"message": "Product not found", "success": False}

    # Add new item to the cart
    new_item = CartItem(
        item_id=item_id,
        item_name="Get name from Oracle Items",
        price=product.price,
        discount=product.discount,
        quantity=1  # Default quantity to 1
    )
    cart.items.append(new_item)
    cart.save()
    return {"message": "Item added to cart", "success": True}

def remove_item(customer_id, item_id):
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        return {"message": "Cart not found", "success": False}

    for item in cart.items:
        if item.item_id == item_id:
            if item.quantity > 1:
                item.quantity -= 1
            else:
                cart.items.remove(item)
            break
    else:
        return {"message": "Item not found in cart", "success": False}

    cart.save()
    return {"message": "Item removed from cart", "success": True}

def clear_item(customer_id, item_id):
    cart = Cart.objects(customer_id=customer_id).first()
    if not cart:
        return {"message": "Cart not found", "success": False}

    for item in cart.items:
        if item.item_id == item_id:
            cart.items.remove(item)
            break
    cart.save()
    return {"message": "Item removed from cart", "success": True}


@cart_bp.route('/cart/confirm_purchase', methods=['POST'])
@login_required
def confirm_purchase():
    customer_id = request.form.get('customer_id')
    voucher_code = request.form.get('voucher_code')

    # Fetch the cart for the current user
    try:
        cart = Cart.objects(customer_id=customer_id).first()
        if not cart or not cart.items:
            return render_template('checkout.html', cart=None, totals=None, error="Your cart is empty."), 400
    except Exception:
        return render_template('checkout.html', error="Cart not found."), 404

    # Fetch the delivery address from the Oracle CUSTOMERS table
    try:
        customer_query = text("SELECT ADDRESS FROM CUSTOMERS WHERE CUSTOMER_ID = :customer_id")
        result = db.session.execute(customer_query, {"customer_id": customer_id}).fetchone()
        if not result:
            return render_template('checkout.html', error="Customer address not found."), 404
        delivery_address = result[0]
    except Exception as e:
        return render_template('checkout.html', error=f"Failed to fetch address: {e}"), 500

    # Generate unique Order ID
    now = datetime.now()
    order_id = f"{customer_id}{now.strftime('%Y%d%m%H%M%S')}"

    # Calculate totals and discounts
    total_price = sum((item.price - item.price * item.discount) * item.quantity for item in cart.items)
    total_discounted = total_price * 0.9 if voucher_code else total_price  # Example: 10% discount for vouchers
    discount = round((total_price - total_discounted) * 100, 2)  # Total discount in percentage

    # Calculate delivery date
    delivery_date = now + timedelta(days=random.randint(1, 15))

    # Set preparation time (in days)
    time_preparation = random.randint(1, 5)

    # Prepare order items
    order_items = []
    for item in cart.items:
        order_items.append(OrderItem(
            Item_ID=item.item_id,
            Quantity=item.quantity,
            Price=item.price
        ))

    # Create the order
    new_order = Order(
        Order_ID=int(order_id),
        Customer_ID=int(customer_id),
        Delivery_Address=delivery_address,
        Payment_Status='Pending',
        Checkout_Total=total_discounted,
        Discount=discount,
        Voucher_code=voucher_code,
        Purchase_date=now,
        Delivery_date=delivery_date,
        Time_preparation=time_preparation,
        Shipping_Status=[{"Status": "processing", "Timestamp": datetime.utcnow()}],
        OrderItems=order_items
    )

    # Save the order to the database
    try:
        new_order.save()

        # Clear the cart
        cart.delete()
    except Exception as e:
        print("merda")
        return render_template('checkout.html', error=f"Failed to create order: {e}"), 500

    # Redirect to the payment page with the order ID
    return render_template('processarPagamento.html', order=new_order)

@cart_bp.route('/cart/purchase_complete', methods=['POST'])
@login_required
def purchase_complete():
    order_id = request.form.get('order')  # Retrieve the order ID from the form

    try:
        print(order_id)
        # Ensure correct type for _id field (adjust based on your _id type in MongoDB)
        order = Order.objects(pk=int(order_id)).first() # Use int if _id is an integer
        # order = Order.objects.get(_id=order_id)  # Use this if _id is a string
        # order = Order.objects.get(_id=ObjectId(order_id))  # Use this if _id is ObjectId

    except (DoesNotExist, ValueError):
        return "Order not found or invalid ID", 404

    # Update Payment_Status to "Complete"
    order.update(set__Payment_Status="Complete")

    # Add shipping status updates
    current_time = datetime.utcnow()
    shipping_status_updates = [
        {"Status": "Complete", "Timestamp": current_time},
        {"Status": "Preparing for Shipping", "Timestamp": current_time + timedelta(hours=1)},
    ]
    order.update(push_all__Shipping_Status=shipping_status_updates)

    # Reload the order to ensure updates are applied
    order.reload()

    # Render the confirmation page
    return render_template('confirmadoPagamento.html', order=order)
