from flask import Blueprint
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user
from .models import (Customer, Employee, Item, Service, SupplierItem, Supplier, Voucher, Warehouse, Zone,
                         PriceHistory, Product, ShippingStatus, OrderItem, Order, Rating, BrowsingHistory)
from flask import Flask, render_template
from flask_login import current_user

admin = Blueprint('admin_warehouse_manager', __name__)

<<<<<<< Updated upstream
@admin.route('/warehouse_manager')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')
=======
from pymongo import MongoClient
from sqlalchemy import create_engine, text
# Initialize MongoDB Client

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['your_mongo_db']

# Initialize SQLAlchemy Engine for Oracle
engine = create_engine('oracle+cx_oracle://username:password@host:port/service_name')



@admin.route('/suppliers')
@login_required
def display_suppliers():
    if current_user.id == 2:
        suppliers = suppliers_best_selling_products()
        if suppliers:
            return render_template('suppliers.html', suppliers=suppliers)
        else:
            return "No suppliers found for the best-selling items."
    return render_template('404.html')


@admin.route('/most_rated_items')
@login_required
def display_most_rated_items():
    if current_user.id == 2:
        items = most_rated_items()
        if items:
            return render_template('most_rated_items.html', items=items)
        else:
            return "No most-rated items found."
    return render_template('404.html')

@admin.route('/low_stock_products')
@login_required
def display_low_stock_products():
    if current_user.id == 2:
        products = products_low_stock()
        if products:
            return render_template('low_stock_products.html', products=products)
        else:
            return "No products have reached their minimum stock level."
    return render_template('404.html')


@admin.route('/aisle_info')
@login_required
def display_aisle_info():
    if current_user.id == 2:
        aisles = aisle_info()
        if aisles:
            return render_template('aisle_info.html', aisles=aisles)
        else:
            return "No aisles found with products having discounts greater than 20%."
    return render_template('404.html')

#US6/7
def suppliers_best_selling_products():
    # MongoDB Aggregation to Find Top 10 Best-Selling Items
    db.orders.aggregate([
        { "$unwind": "$OrderItems" },
        {
            "$group": {
                "_id": "$OrderItems.FK_Item_ID",
                "total_quantity": { "$sum": "$OrderItems.Quantity" }
            }
        },
        { "$sort": { "total_quantity": -1 } },
        { "$limit": 10 },
        {
            "$lookup": {
                "from": "Products",
                "localField": "_id",
                "foreignField": "Item_ID",
                "as": "product_details"
            }
        },
        {
            "$project": {
                "_id": 0,
                "item_id": "$_id",
                "total_quantity": 1
            }
        },
        { "$out": "top_selling_products" }  # Save results in a new collection
    ])

    # Retrieve the Top 10 Item IDs from MongoDB
    top_items = list(db.top_selling_products.find({}, {"_id": 0, "item_id": 1}))
    top_item_ids = [str(item["item_id"]) for item in top_items]

    if not top_item_ids:
        return []

    # Oracle SQL Query to Get Supplier Names for the Best-Selling Items
    query = text(f"""
        SELECT DISTINCT s.name
        FROM Suppliers s
        JOIN SupplierItems si ON s.Supplier_ID = si.Supplier_ID
        JOIN Items i ON i.Item_ID = si.Item_ID
        WHERE i.Item_ID IN ({', '.join([f"'{item_id}'" for item_id in top_item_ids])})
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        supplier_names = [row[0] for row in result.fetchall()]

    return supplier_names

#US8
def most_rated_items():
    # MongoDB Aggregation to Find Top 10 Most-Rated Items
    db.ratings.aggregate([
        {
            "$group": {
                "_id": "$item_id",
                "vote_count": {"$sum": 1}
            }
        },
        {"$sort": {"vote_count": -1}},
        {"$limit": 10},
        {
            "$lookup": {
                "from": "Products",
                "localField": "_id",
                "foreignField": "Item_ID",
                "as": "product_details"
            }
        },
        {
            "$project": {
                "_id": 0,
                "item_id": "$_id",
                "vote_count": 1
            }
        },
        {"$out": "most_rated_products"}  # Save results in a new collection
    ])

    # Retrieve the Top 10 Item IDs from MongoDB
    most_rated_items = list(db.most_rated_products.find({}, {"_id": 0, "item_id": 1}))
    most_rated_item_ids = [str(item["item_id"]) for item in most_rated_items]

    if not most_rated_item_ids:
        return []

    # Oracle SQL Query to Get Item Details and Supplier Names
    query = text(f"""
        SELECT DISTINCT
            i.Item_ID,
            i.Name AS Item_Name,
            s.Name AS Supplier_Name
        FROM Items i
        JOIN SupplierItems si ON i.Item_ID = si.Item_ID
        JOIN Suppliers s ON si.Supplier_ID = s.Supplier_ID
        WHERE i.Item_ID IN ({', '.join([f"'{item_id}'" for item_id in most_rated_item_ids])})
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        item_supplier_details = [
            {
                "item_id": row[0],
                "item_name": row[1],
                "supplier_name": row[2]
            } for row in result.fetchall()
        ]

    return item_supplier_details


#US9
def products_low_stock():
    # MongoDB Aggregation to Find Products with Low Stock
    db.products.aggregate([
        {
            "$match": {
                "$expr": {
                    "$lte": ["$Quantity_in_Stock", "$Minimum_Stock"]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "item_id": "$Item_ID",
                "quantity_in_stock": "$Quantity_in_Stock",
                "minimum_stock": "$Minimum_Stock"
            }
        },
        {"$out": "products_below_stock"}  # Save results in a new collection
    ])

    # Retrieve Low-Stock Items from MongoDB
    products_below_stock = list(db.products_below_stock.find({}, {
        "item_id": 1,
        "quantity_in_stock": 1,
        "minimum_stock": 1,
        "_id": 0
    }))

    if not products_below_stock:
        return []

    # Generate Conditions for Oracle SQL Query
    conditions = " OR ".join(
        f"(i.Item_ID = '{product['item_id']}' AND p.Quantity_in_Stock = {product['quantity_in_stock']} AND p.Minimum_Stock = {product['minimum_stock']})"
        for product in products_below_stock
    )

    # Oracle SQL Query to Get Product and Supplier Information
    query = text(f"""
        SELECT 
            i.Item_Description,
            i.Name AS Item_Name,
            i.Brand,
            p.Quantity_in_Stock,
            p.Minimum_Stock,
            s.Name AS Supplier_Name
        FROM Items i
        JOIN SupplierItems si ON i.Item_ID = si.Item_ID
        JOIN Suppliers s ON si.Supplier_ID = s.Supplier_ID
        JOIN Products p ON i.Item_ID = p.Item_ID
        WHERE {conditions}
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        low_stock_products = [
            {
                "description": row[0],
                "item_name": row[1],
                "brand": row[2],
                "quantity_in_stock": row[3],
                "minimum_stock": row[4],
                "supplier_name": row[5]
            } for row in result.fetchall()
        ]

    return low_stock_products

#US10
def aisle_info():
    # Step 1: MongoDB Aggregation to Find Items with Discount > 20%
    greater_discount = list(db.Orders.aggregate([
        {"$match": {"discount": {"$gt": 20}}},  # Filter orders with discount greater than 20%
        {"$unwind": "$OrderItems"},             # Unwind the order items array
        {
            "$group": {
                "_id": "$OrderItems.FK_Item_ID",  # Group by Item ID
                "total_orders": {"$sum": 1}       # Count the number of orders per item
            }
        },
        {"$sort": {"total_orders": -1}}          # Sort by total orders in descending order
    ]))

    # Extract the item IDs
    greater_discount_ids = [item["_id"] for item in greater_discount]

    # Step 2: Find Aisle IDs for these items in the Products Collection
    greater_discount_aisles = list(db.Products.find(
        {"Product_ID": {"$in": greater_discount_ids}},  # Find products with matching Product_IDs
        {"_id": 0, "Product_Aisle_ID": 1}               # Only retrieve Product_Aisle_ID
    ))

    # Extract the aisle IDs
    aisles_id = [item["Product_Aisle_ID"] for item in greater_discount_aisles]

    if not aisles_id:
        return []

    # Step 3: Oracle SQL Query to Retrieve Aisle Information
    placeholders = ', '.join(f"'{aisle}'" for aisle in aisles_id)  # Format aisle IDs for SQL query
    oracle_query_US10 = text(f"""
        SELECT 
            a.Aisle_ID,
            a.Capacity,
            a.Warehouse_ID,
            a.Zone_ID
        FROM Aisles a
        WHERE a.Aisle_ID IN ({placeholders})
    """)

    # Execute the query and fetch results
    with engine.connect() as connection:
        result = connection.execute(oracle_query_US10)
        aisle_details = [
            {
                "aisle_id": row[0],
                "capacity": row[1],
                "warehouse_id": row[2],
                "zone_id": row[3]
            } for row in result.fetchall()
        ]

    return aisle_details
>>>>>>> Stashed changes
