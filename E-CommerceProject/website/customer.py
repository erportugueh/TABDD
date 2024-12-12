from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_required
from .models import Order, Item
from datetime import datetime
from .models import Rating

customer = Blueprint('customer', __name__)

@customer.route('/profile/<int:customer_id>')
@login_required
def profile_view(customer_id):

    return render_template('userDetails.html')

@customer.route('/activeOrders/<int:customer_id>')
@login_required
def active_orders(customer_id):
    # Ensure the current user matches the customer_id
    if current_user.customer_id != customer_id:
        return "Unauthorized", 403

    # Query the Orders collection
    orders = Order.objects(
        Customer_ID=current_user.customer_id,  # Match the customer ID
        Shipping_Status__not__match={"Status": "Delivered"}  # Check if the last Shipping_Status is not 'Delivered'
    ).order_by("-Shipping_Status__Timestamp")  # Ensure the latest status is checked

    # Add item names from Oracle
    for order in orders:
        for item in order.OrderItems:
            item_id = item["Item_ID"]  # Fetch the Item_ID
            # Query Oracle for the item name
            result = Item.query.filter_by(item_id=item_id).first()  # Use correct variable
            if result:
                item.name = result.name  # Append the name to the item
    # Render the template with the enriched orders
    return render_template('userActiveOrders.html', orders=orders)

@customer.route('/OrdersReviews/<int:customer_id>')
@login_required
def orders_reviews(customer_id):
    # Ensure the current user matches the customer_id
    if current_user.customer_id != customer_id:
        return "Unauthorized", 403

    # Query the Orders collection
    orders = Order.objects(
        Customer_ID=current_user.customer_id,  # Match the customer ID
        Shipping_Status__match={"Status": "Delivered"}  # Check if the last Shipping_Status is not 'Delivered'
    ).order_by("-Shipping_Status__Timestamp")  # Ensure the latest status is checked

    # Add item names from Oracle
    for order in orders:
        for item in order.OrderItems:
            item_id = item["Item_ID"]  # Fetch the Item_ID
            # Query Oracle for the item name
            result = Item.query.filter_by(item_id=item_id).first()  # Use correct variable
            if result:
                item.name = result.name  # Append the name to the item
    # Render the template with the enriched orders
    return render_template('userOrdersReview.html', orders=orders)

@customer.route('/submit_comment', methods=['POST'])
@login_required
def submit_comment():
    # Extract form data
    item_id = request.form.get('item_id')
    comment = request.form.get('comment')
    rating = request.form.get('rating')

    # Validate inputs
    if not item_id or not rating:
        flash("Item ID and rating are required.", "error")
        return redirect(url_for('customer.active_orders', customer_id=current_user.customer_id))

    try:
        # Ensure rating is an integer within the valid range
        rating = int(rating)
        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.", "error")
            return redirect(url_for('customer.active_orders', customer_id=current_user.customer_id))

        # Check if a review already exists
        existing_review = Rating.objects(
            customer_id=current_user.customer_id,
            item_id=int(item_id)
        ).first()

        if existing_review:
            # Update the existing review
            existing_review.update(
                set__rating=rating,
                set__comment=comment if comment else None
            )
            flash("Your review has been updated successfully!", "success")
        else:
            # Create a new review
            new_rating = Rating(
                customer_id=current_user.customer_id,
                item_id=int(item_id),
                rating=rating,
                comment=comment if comment else None
            )
            new_rating.save()
            flash("Your review has been submitted successfully!", "success")

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('customer.active_orders', customer_id=current_user.customer_id))

    # Redirect to the Order Reviews page
    return redirect(url_for('customer.orders_reviews', customer_id=current_user.customer_id))