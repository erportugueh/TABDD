from flask import Blueprint, render_template
from flask_login import current_user, login_required

customer = Blueprint('customer', __name__)

@customer.route('/profile/<int:customer_id>')
@login_required
def profile_view(customer_id):

    return render_template('userDetails.html')

@customer.route('/activeOrders/<int:customer_id>')
@login_required
def active_orders(customer_id):

    return render_template('userActiveOrders.html')

@customer.route('/OrdersReviews/<int:customer_id>')
@login_required
def orders_reviews(customer_id):

    return render_template('userOrdersReview.html')