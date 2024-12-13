from flask import Blueprint, render_template, redirect, request, url_for, flash  # Import Flask modules for blueprint and routing
from flask_login import current_user, login_required  # Import login functions for user session management
from .models import Order, Item, Rating  # Import models for database interaction

# Define the 'customer' blueprint
customer = Blueprint('customer', __name__)

@customer.route('/profile/<int:customer_id>')
@login_required  # Ensure the user is logged in before accessing this route
def profile_view(customer_id):
    # Render the user profile page
    return render_template('userDetails.html')

@customer.route('/activeOrders/<int:customer_id>')
@login_required  # Ensure the user is logged in before accessing this route
def active_orders(customer_id):
    # Ensure the current user matches the requested customer ID
    if current_user.customer_id != customer_id:
        return "Unauthorized", 403  # Return 403 Forbidden if IDs don't match

    # Query MongoDB for orders where the last shipping status is not 'Delivered'
    orders = Order.objects(
        Customer_ID=current_user.customer_id,  # Filter orders by customer ID
        Shipping_Status__not__match={"Status": "Delivered"}  # Exclude delivered orders
    ).order_by("-Shipping_Status__Timestamp")  # Order by the most recent shipping status timestamp

    # Add item names from the Oracle database
    for order in orders:
        for item in order.OrderItems:  # Loop through each item in the order
            item_id = item["Item_ID"]  # Get the item ID
            # Query Oracle database for the item name
            result = Item.query.filter_by(item_id=item_id).first()
            if result:
                item.name = result.name  # Add the item name to the item

    # Render the user's active orders page with enriched order data
    return render_template('userActiveOrders.html', orders=orders)

@customer.route('/OrdersReviews/<int:customer_id>')
@login_required  # Ensure the user is logged in before accessing this route
def orders_reviews(customer_id):
    # Ensure the current user matches the requested customer ID
    if current_user.customer_id != customer_id:
        return "Unauthorized", 403  # Return 403 Forbidden if IDs don't match

    # Query MongoDB for orders where the last shipping status is 'Delivered'
    orders = Order.objects(
        Customer_ID=current_user.customer_id,  # Filter orders by customer ID
        Shipping_Status__match={"Status": "Delivered"}  # Include only delivered orders
    ).order_by("-Shipping_Status__Timestamp")  # Order by the most recent shipping status timestamp

    # Add item names from the Oracle database
    for order in orders:
        for item in order.OrderItems:  # Loop through each item in the order
            item_id = item["Item_ID"]  # Get the item ID
            # Query Oracle database for the item name
            result = Item.query.filter_by(item_id=item_id).first()
            if result:
                item.name = result.name  # Add the item name to the item

    # Render the user's order reviews page with enriched order data
    return render_template('userOrdersReview.html', orders=orders)

@customer.route('/submit_comment', methods=['POST'])
@login_required  # Ensure the user is logged in before accessing this route
def submit_comment():
    # Extract form data from the request
    item_id = request.form.get('item_id')  # Get the item ID from the form
    comment = request.form.get('comment')  # Get the comment from the form
    rating = request.form.get('rating')  # Get the rating from the form

    # Validate inputs
    if not item_id or not rating:  # Ensure item ID and rating are provided
        flash("Item ID and rating are required.", "error")  # Display error message
        return redirect(url_for('customer.active_orders', customer_id=current_user.customer_id))

    try:
        # Convert rating to integer and validate its range
        rating = int(rating)
        if rating < 1 or rating > 5:  # Check if rating is between 1 and 5
            flash("Rating must be between 1 and 5.", "error")  # Display error message
            return redirect(url_for('customer.active_orders', customer_id=current_user.customer_id))

        # Check if a review already exists for the item
        existing_review = Rating.objects(
            customer_id=current_user.customer_id,  # Match customer ID
            item_id=int(item_id)  # Match item ID
        ).first()

        if existing_review:
            # Update the existing review with new rating and comment
            existing_review.update(
                set__rating=rating,
                set__comment=comment if comment else None
            )
            flash("Your review has been updated successfully!", "success")  # Display success message
        else:
            # Create a new review
            new_rating = Rating(
                customer_id=current_user.customer_id,  # Set customer ID
                item_id=int(item_id),  # Set item ID
                rating=rating,  # Set rating
                comment=comment if comment else None  # Set comment if provided
            )
            new_rating.save()  # Save the new review
            flash("Your review has been submitted successfully!", "success")  # Display success message

    except Exception as e:
        # Handle errors during the review process
        flash(f"An error occurred: {str(e)}", "error")  # Display error message
        return redirect(url_for('customer.active_orders', customer_id=current_user.customer_id))

    # Redirect to the order reviews page
    return redirect(url_for('customer.orders_reviews', customer_id=current_user.customer_id))
