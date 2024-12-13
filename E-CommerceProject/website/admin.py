from flask_login import login_required
from flask import Blueprint, jsonify, render_template, request
from pymongo import MongoClient
import pytz
import logging
from sqlalchemy import text
from datetime import datetime
from .models import Item, Customer
from . import db
admin = Blueprint('admin', __name__)

# String de conexão
connection_string = "mongodb://ecommerce_user:secure_password@vsgate-s1.dei.isep.ipp.pt:10911/EcommerceDB"

# Conectar ao servidor MongoDB
client = MongoClient(connection_string)

# Acessar o banco de dados
dbmongo = client["EcommerceDB"]

@admin.route('/manager', methods=['GET'])
def admin_manager():
    return render_template('adminManager.html')

@admin.route('/manager/queryUS13', methods=['GET'])
def query_us13():
    # MongoDB aggregation pipeline
    pipeline_us13 = [
        {"$match": {"Voucher_code": {"$exists": True, "$ne": None}}},
        {"$group": {
            "_id": "$Customer_ID",
            "total_count_vouchers": {"$sum": 1}
        }},
        {"$sort": {"total_count_vouchers": -1}},
        {"$limit": 1}
    ]
    top_voucher_customer = list(dbmongo.Orders.aggregate(pipeline_us13))
    print(top_voucher_customer)

    if top_voucher_customer:
        top_client_id = top_voucher_customer[0]['_id']
        order_items = dbmongo.Orders.find_one({"Customer_ID" : top_client_id},{"OrderItems" : 1, "_id" : 0})

        # Fetch the customer name from Oracle
        customer = Customer.query.filter_by(customer_id=top_client_id).first()

        # Add item names to order items
        enriched_order_items = []
        for product in order_items.get("OrderItems", []):
            item = Item.query.filter_by(item_id=product["Item_ID"]).first()
            enriched_order_items.append({
                "Item_ID": product["Item_ID"],
                "Quantity": product["Quantity"],
                "Price": product["Price"],
                "Item_Name": item.name if item else "Unknown"
            })

        # Debugging Output
        print(
            f"Top Client: {top_client_id}, Customer Name: {customer.name if customer else 'Unknown'}, Orders: {enriched_order_items}")

        return jsonify({
            "top_client_id": top_client_id,
            "customer_name": customer.name if customer else "Unknown",
            "total_vouchers": top_voucher_customer[0]['total_count_vouchers'],
            "order_items": enriched_order_items
        })
    else:
        return jsonify({"error": "No voucher clients found"}), 404


@admin.route('/manager/queryUS14', methods=['GET'])
def query_us14():
    # Define the date range
    start_date = datetime(2024, 6, 1, 0, 0, 0, tzinfo=pytz.UTC)
    end_date = datetime(2024, 8, 17, 23, 59, 59, tzinfo=pytz.UTC)

    # MongoDB query
    result_US14 = list(dbmongo.Orders.find(
        {
            "Purchase_date": {"$gte": start_date, "$lte": end_date},
            "Preparation_time": {"$lt": 10},
            "$expr": {
                "$gt": [
                    {"$subtract": ["$Delivery_date", "$Purchase_date"]},
                    10 * 24 * 60 * 60 * 1000  # 10 days in milliseconds
                ]
            }
        },
        {"_id": 1, "Customer_ID": 1, "Purchase_date": 1, "Delivery_date": 1}
    ))
    print(result_US14)
    # Enrich results with customer names from Oracle
    enriched_results = []
    for order in result_US14:
        # Get the customer's name from Oracle
        print(order["Purchase_date"])
        customer = Customer.query.filter_by(customer_id=order["Customer_ID"]).first()
        enriched_results.append({
            "Order_ID": order["_id"],
            "Customer_Name": customer.name if customer else "Unknown",
            "Purchase_Date": order["Purchase_date"],
            "Delivery_Date": order["Delivery_date"]
        })

    return jsonify(enriched_results)

@admin.route('/deliveryOrderManager')
@login_required
def delivery_order_manager():
    return render_template('adminDeliveryOrderManager.html')

@admin.route('/deliveryOrderManager/queryUS11', methods=['POST'])
@login_required
def query_us11():
    from datetime import datetime
    import pytz

    # Get filters from the request
    data = request.json
    date = data.get("date")
    time = data.get("time")

    if not date or not time:
        return jsonify({"error": "Date and time are required"}), 400

    try:
        # Combine date and time to a single datetime object
        date_time_str = f"{date}T{time}:00.000+00:00"
        date_and_time = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        print(date_and_time)
        print(int(data.get("name")))
        # MongoDB aggregation pipeline
        result_US11 = list(dbmongo.Orders.aggregate([
            {"$unwind": "$Shipping_Status"},  # Unwind the Shipping_Status array
            {"$match": {
                "Shipping_Status.Timestamp": {"$lt": date_and_time},  # Filter statuses before the provided datetime
                "_id": int(data.get("name"))  # Ensure order ID matches
            }},
            {"$sort": {"Shipping_Status.Timestamp": -1}},  # Sort by most recent timestamp
            {"$limit": 1},  # Get the latest shipping status before the provided datetime
            {"$project": {
                "Status": "$Shipping_Status.Status",
                "Location": "$Shipping_Status.Location",
                "Timestamp": "$Shipping_Status.Timestamp"
            }}
        ]))
        print(result_US11)
        if not result_US11:
            return jsonify({"error": "No matching orders found"}), 404

        return jsonify(result_US11[0])

    except ValueError as e:
        logging.error(f"Invalid date or time format: {e}")
        return jsonify({"error": "Invalid date or time format"}), 400
    except Exception as e:
        logging.error(f"Error in US11: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@admin.route('/deliveryOrderManager/queryUS12', methods=['POST'])
@login_required
def query_us12():
    # Get order ID from the request
    data = request.json
    order_id = data.get("order_id")
    try:
        # MongoDB aggregation pipeline
        result_US12 = list(dbmongo.Orders.aggregate([
            {"$match": {"_id": int(order_id)}},  # Match order by ID
            {"$unwind": "$Shipping_Status"},  # Unwind the Shipping_Status array
            {"$sort": {"Shipping_Status.Timestamp": 1}},  # Sort by timestamp
            {"$project": {  # Include relevant fields in the output
                "_id": 1,
                "Shipping_Status.Status": 1,
                "Shipping_Status.Location": 1,
                "Shipping_Status.Timestamp": 1
            }}
        ]))

        # Handle no results
        if not result_US12:
            logging.debug(f"No results found for order ID: {order_id}")
            return jsonify({"error": "No shipping information found for the provided order ID"}), 404

        # Log and return the results
        logging.debug(f"US12 Results: {result_US12}")
        return jsonify(result_US12)

    except Exception as e:
        logging.error(f"Error in US12: {e}")
        return jsonify({"error": "Invalid order ID"}), 400

@admin.route('/warehouseManager')
@login_required
def warehouse_manager():
    return render_template('adminWarehouseManager.html')

@admin.route('/warehouseManager/queryUS7', methods=['GET'])
@login_required
def query_us7():
    try:
        # Step 1: Aggregate query in MongoDB
        top_items = list(dbmongo.Orders.aggregate([
            {"$unwind": "$OrderItems"},
            {
                "$group": {
                    "_id": "$OrderItems.Item_ID",
                    "total_quantity": {"$sum": "$OrderItems.Quantity"},
                    "purchase_dates": {"$addToSet": "$Purchase_date"}
                }
            },
            {"$sort": {"total_quantity": -1}},
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
                    "total_quantity": 1,
                    "purchase_dates": 1
                }
            },
        ]))

        # Step 2: Extract Item IDs from the MongoDB query results
        top_item_ids = [str(item["item_id"]) for item in top_items if item.get("item_id") is not None]
        if not top_item_ids:
            return jsonify({"error": "No top-selling items found."}), 404

        # Step 3: Build dynamic IN clause
        placeholders = ", ".join([f":item_{i}" for i in range(len(top_item_ids))])
        oracle_query = f"""
            SELECT si.ITEM_ID AS item_id, s.NAME AS supplier_name
            FROM SUPPLIERS s
            JOIN SUPPLIERITEMS si ON s.SUPPLIER_ID = si.SUPPLIER_ID
            WHERE si.ITEM_ID IN ({placeholders})
        """

        # Map top_item_ids to individual placeholders
        params = {f"item_{i}": item_id for i, item_id in enumerate(top_item_ids)}

        # Execute the query and fetch results
        oracle_result = db.session.execute(text(oracle_query), params).mappings().all()
        print(oracle_result)
        # Process the results
        suppliers = [{"item_id": row["item_id"], "supplier_name": row["supplier_name"]} for row in oracle_result]
        print(suppliers)
        # Combine MongoDB and Oracle results
        combined_results = []
        for item in top_items:
            suppliers_for_item = [supplier for supplier in suppliers if supplier["item_id"] == item["item_id"]]
            print(suppliers_for_item)
            combined_results.append({
                "item_id": item["item_id"],
                "total_quantity": item["total_quantity"],
                "purchase_dates": item["purchase_dates"],
                "suppliers": suppliers_for_item
            })

        return jsonify(combined_results)

    except Exception as e:
        logging.error(f"Error in US7: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@admin.route('/warehouseManager/queryUS8', methods=['GET'])
@login_required
def query_us8():
    try:
        # Step 1: Aggregate query in MongoDB for top-rated items and their average rating
        top_rated_items = list(dbmongo.Ratings.aggregate([
            {"$group": {
                "_id": "$item_id",
                "vote_count": {"$sum": 1},
                "average_rating": {"$avg": "$rating"}
            }},
            {"$sort": {"vote_count": -1}},
            {"$limit": 10},
            {"$project": {
                "_id": 0,
                "item_id": "$_id",
                "vote_count": 1,
                "average_rating": {"$round": ["$average_rating", 2]}
            }}
        ]))

        # Step 2: Extract item IDs and prepare mapping of vote counts and average ratings
        top_rated_item_ids = [item["item_id"] for item in top_rated_items]
        if not top_rated_item_ids:
            return jsonify({"error": "No top-rated items found."}), 404

        items_id_str = ', '.join([str(i) for i in top_rated_item_ids])
        item_votes = {item["item_id"]: {"vote_count": item["vote_count"], "average_rating": item["average_rating"]} for item in top_rated_items}

        # Step 3: Query Oracle for item and supplier details
        oracle_query = f"""
            SELECT 
                i.Item_ID AS item_id, 
                i.Name AS item_name, 
                s.Name AS supplier_name
            FROM Items i
            JOIN SupplierItems si ON i.Item_ID = si.Item_ID
            JOIN Suppliers s ON si.Supplier_ID = s.Supplier_ID
            WHERE i.Item_ID IN ({items_id_str})
        """

        # Use SQLAlchemy's connection to execute the query
        oracle_result = db.session.execute(text(oracle_query))

        # Step 4: Process the Oracle results
        suppliers_by_item = {}
        for row in oracle_result:
            item_id = row[0]
            if item_id not in suppliers_by_item:
                suppliers_by_item[item_id] = []
            suppliers_by_item[item_id].append(row[2])  # Append supplier name

        # Step 5: Combine results with vote counts and average ratings
        result_us8 = []
        for item_id, details in item_votes.items():
            result_us8.append({
                "Item_ID": item_id,
                "Vote_Count": details["vote_count"],
                "Average_Rating": details["average_rating"],
                "Suppliers": suppliers_by_item.get(item_id, [])
            })

        # Sort the results by Average_Rating in descending order
        sorted_results = sorted(result_us8, key=lambda x: x["Average_Rating"], reverse=True)

        return jsonify(sorted_results)

    except Exception as e:
        logging.error(f"Error in US8: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@admin.route('/warehouseManager/queryUS9', methods=['GET'])
@login_required
def query_us9():
    try:
        # Step 1: Query MongoDB for products below minimum stock level
        products_below_stock = list(dbmongo.Products.aggregate([
            {
                "$match": {
                    "$expr": {
                        "$lte": ["$quantity_in_stock", "$minimum_stock"]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "item_id": 1,
                    "quantity_in_stock": 1,
                    "minimum_stock": 1
                }
            }
        ]))

        if not products_below_stock:
            logging.error("No products below minimum stock found in MongoDB.")
            return jsonify({"error": "No products below minimum stock level found."}), 404

        # Extract item IDs and map MongoDB data
        item_data = {product["item_id"]: product for product in products_below_stock if "item_id" in product}
        item_ids = list(item_data.keys())

        if not item_ids:
            logging.error("No valid item IDs found in MongoDB results.")
            return jsonify({"error": "No valid items found below minimum stock level."}), 404

        # Prepare item IDs for Oracle query
        item_ids_str = ", ".join(map(str, item_ids))

        # Step 2: Query Oracle for product details and suppliers
        oracle_query = f"""
            SELECT 
                i.Item_ID AS item_id,
                i.Name AS item_name,
                i.Brand AS brand,
                s.Name AS supplier_name
            FROM Items i
            JOIN SupplierItems si ON i.Item_ID = si.Item_ID
            JOIN Suppliers s ON si.Supplier_ID = s.Supplier_ID
            WHERE i.Item_ID IN ({item_ids_str})
        """

        oracle_result = db.session.execute(text(oracle_query)).fetchall()

        # Combine MongoDB and Oracle results
        suppliers_map = {}
        for row in oracle_result:
            item_id = row[0]
            if item_id not in suppliers_map:
                suppliers_map[item_id] = {
                    "Item_ID": item_id,
                    "Item_Name": row[1],
                    "Brand": row[2],
                    "Suppliers": []
                }
            suppliers_map[item_id]["Suppliers"].append(row[3])

        result_us9 = []
        for item_id, data in suppliers_map.items():
            product_data = item_data.get(item_id, {})
            result_us9.append({
                "Item_ID": data["Item_ID"],
                "Item_Name": data["Item_Name"],
                "Brand": data["Brand"],
                "Quantity_in_Stock": product_data.get("quantity_in_stock", "N/A"),
                "Minimum_Stock": product_data.get("minimum_stock", "N/A"),
                "Suppliers": ", ".join(data["Suppliers"])  # Combine supplier names into one string
            })

        # Validate final results
        if not result_us9:
            logging.error("No valid data combined from MongoDB and Oracle.")
            return jsonify({"error": "No valid data found for products below minimum stock level."}), 404

        return jsonify(result_us9)

    except Exception as e:
        logging.error(f"Error in US9: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@admin.route('/warehouseManager/queryUS10', methods=['GET'])
@login_required
def query_us10():
    try:
        # Step 1: Aggregate query in MongoDB to find products with discounts > 20%
        greater_discount = list(dbmongo.Orders.aggregate([
            {"$unwind": "$OrderItems"},  # Decompose OrderItems array
            {"$match": {"OrderItems.Discount": {"$gt": 0.2}}},  # Match items with a discount > 20%
            {
                "$group": {
                    "_id": "$OrderItems.Item_ID",  # Group by Item_ID
                    "total_quantity": {"$sum": "$OrderItems.Quantity"},  # Sum total quantities
                    "discounts": {"$addToSet": "$OrderItems.Discount"}  # Collect unique discounts
                }
            },
            {"$sort": {"total_quantity": -1}}  # Sort by total quantity (descending)
        ]))

        # Step 2: Extract Item IDs and Discounts
        greater_discount_ids = [item["_id"] for item in greater_discount]
        discount_map = {item["_id"]: item["discounts"] for item in greater_discount}
        quantity_map = {item["_id"]: item["total_quantity"] for item in greater_discount}

        if not greater_discount_ids:
            return jsonify({"error": "No products with discounts greater than 20% found."}), 404

        # Step 3: Query Oracle DB for product and aisle details
        item_ids_str = ', '.join(map(str, greater_discount_ids))
        oracle_query = f"""
            SELECT 
                i.Item_ID AS item_id,
                i.Name AS product_name,
                a.Aisle_ID AS aisle_id,
                a.Warehouse_ID AS warehouse_id,
                a.Zone_ID AS zone_id
            FROM Items i
            LEFT JOIN SupplierItems si ON i.Item_ID = si.Item_ID
            LEFT JOIN Aisles a ON si.Supplier_ID = a.Aisle_ID
            WHERE i.Item_ID IN ({item_ids_str})
        """

        # Execute the query using SQLAlchemy
        oracle_result = db.session.execute(text(oracle_query)).fetchall()

        # Step 4: Process Oracle results
        result_map = {
            row.item_id: {
                "Product_Name": row.product_name,
                "Warehouse_ID": row.warehouse_id,
                "Zone_ID": row.zone_id,
                "Aisle_ID": row.aisle_id
            }
            for row in oracle_result
        }

        # Step 5: Combine MongoDB and Oracle results
        combined_results = []
        for item_id in greater_discount_ids:
            if item_id in result_map:
                product_details = result_map[item_id]
                combined_results.append({
                    "Product_ID": item_id,
                    "Product_Name": product_details.get("Product_Name", "Unknown"),
                    "Warehouse_ID": product_details.get("Warehouse_ID"),
                    "Zone_ID": product_details.get("Zone_ID"),
                    "Aisle_ID": product_details.get("Aisle_ID"),
                    "Discounts": [f"{(d * 100):.2f}%" for d in discount_map.get(item_id, [])],  # Format discounts with %
                    "Total_Quantity": quantity_map.get(item_id, 0)
                })

        if not combined_results:
            return jsonify({"error": "No matching data found."}), 404

        return jsonify(combined_results)

    except Exception as e:
        logging.error(f"Error in US10: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@admin.route('/cio')
@login_required
def cio():
    return render_template('adminCIO.html')


@admin.route('/profileEmployee/<int:employee_id>')
@login_required
def profile_employee_view(employee_id):

    return render_template('employeeDetails.html')