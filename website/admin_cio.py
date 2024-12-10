from flask import Blueprint

<<<<<<< Updated upstream
admin = Blueprint('admin_cio', __name__)
=======
admin = Blueprint('admin_cio', __name__)

admin = Blueprint('admin_warehouse_manager', __name__)

@admin.route('/manager')
@login_required
def display_customers():

        customers = Customer.query.all()
        return "render_template('customers.html', customers=customers)"
>>>>>>> Stashed changes
