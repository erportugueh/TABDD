from bson import ObjectId
from website.models import Product, Customer, PriceHistory
from website import db
from mongoengine.errors import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def insert_product_with_specific_id(app, product_id):
    with app.app_context():
        try:
            # Use a specific _id
            specific_id = product_id

            # Check if the document with this _id already exists
            if Product.objects(_id=specific_id).first():
                print(f"Product with _id {specific_id} already exists.")
                return

            # Create a new product with a specific _id
            product = Product(
                _id=specific_id,  # Specify the _id explicitly
                item_id=101,
                product_warehouse_id=1,
                product_zone_id=1,
                quantity_in_stock=50,
                minimum_stock=10,
                price=19.99,
                category="Electronics",
                subcategory="Headphones",
                discount=0.01,
                price_history=[
                    PriceHistory(price=19.99, changed_at=datetime.now(), reason="Initial Price")
                ]
            )

            # Save the document
            product.save()
            print(f"Product with _id {product_id} inserted into MongoDB successfully.")
        except ValidationError as e:
            print(f"Validation failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def insert_customer_to_oracle():
    try:
        # Create a new Customer instance
        customer = Customer(
            customer_id=1,
            name="John Doe",
            address="123 Main St",
            postal_code="12345",
            nif="123456789",
            email="johndoe@example.com",
            account_id=1,
            password_hash="",
            gdpr_terms="Accepted",
            accepted_date=datetime.utcnow(),
            points_balance=100,
            last_points_redeemed_date=None,
            status="Active"
        )
        # Set the password using the property
        customer.password = "secure_password"

        # Add and commit to Oracle database
        db.session.add(customer)
        db.session.commit()
        print("Customer inserted into Oracle database successfully.")
    except SQLAlchemyError as e:
        print(f"Failed to insert customer into Oracle database: {e}")
        db.session.rollback()

if __name__ == "__main__":
    insert_product_to_mongodb()
    insert_customer_to_oracle()
