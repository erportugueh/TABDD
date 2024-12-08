import cx_Oracle

from datetime import datetime, timezone
import hashlib
from pymongo import MongoClient



 # Database connection parameters
host = "vsgate-s1.dei.isep.ipp.pt"
port = "10434"
sid = "xe"
dsn_tns = cx_Oracle.makedsn(host, port, sid)
username = "C##e_commerce"  # Replace with your database username
password = "qKCH1brdHfWtMFadWdbzWeMJS3rHDJ"  # Replace with your database password
connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
cursor = connection.cursor()

# MongoDB Connection String
connection_string = "mongodb://ecommerce_user:secure_password@vsgate-s1.dei.isep.ipp.pt:10911/EcommerceDB"
client = MongoClient(connection_string)
db = client["EcommerceDB"]
ratings_collection = db["Ratings"]
browsing_collection = db["BrowsingHistory"]


class Database():

    # Function to save customer data into the database
    def save_customer_to_db(self, customer_data):
        try:
           
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()
            # Insert SQL command
            insert_query = """
            INSERT INTO Customers (
                Name, Address, Postal_Code, NIF, Email, Account_ID, Password_Hash,
                GDPR_Terms, Accepted_Date, Points_Balance, Status
            ) VALUES (
                :name, :address, :postal_code, :nif, :email, :account_id, :password_hash,
                :gdpr_terms, :accepted_date, :points_balance, :status
            )
            """

            # Execute the query with customer data
            cursor.execute(insert_query, customer_data)
            connection.commit()

            print("Customer registered successfully!")

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
    

    def verify_login(self, usernamelogin, passwordlogin):

        try:
            # Connect to the Oracle database
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            # Hash the input password to compare with stored hashes
            hashed_password = hashlib.sha256(passwordlogin.encode()).hexdigest()

            # Check if the user is an employee
            employee_query = """
                SELECT Name, Account_ID, Email, Role
                FROM Employees
                WHERE Name = :usernamelogin
                AND Password_Hash = :password_hash
            """
            cursor.execute(employee_query, {'usernamelogin': usernamelogin, 'password_hash': hashed_password})
            employee = cursor.fetchone()

            if employee:
                return {
                    'name': employee[0],
                    'account_id': employee[1],
                    'email': employee[2],
                    'role': employee[3],
                    'type': 'employee'
                }

            # Check if the user is a customer
            customer_query = """
                SELECT Name, Account_ID, Email, Points_Balance, Status
                FROM Customers
                WHERE Name = :usernamelogin
                AND Password_Hash = :password_hash
            """
            cursor.execute(customer_query, {'usernamelogin': usernamelogin, 'password_hash': hashed_password})
            customer = cursor.fetchone()

            if customer:
                return {
                    'name': customer[0],
                    'account_id': customer[1],
                    'email': customer[2],
                    'points_balance': customer[3],
                    'status': customer[4],
                    'type': 'customer'
                }

        except cx_Oracle.DatabaseError as e:
            print(f"Error during login verification: {e}")
            return None

        finally:
            # Clean up resources
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

        return None
    def get_next_account_id(self):
        """
        Fetch the next value from the AccountID_Sequence in the database.
        :return: The next Account_ID as an integer.
        """
        try:
            # Connect to the database
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            # Query to fetch the next sequence value
            query = "SELECT MAX(Account_ID) AS MaxAccountID FROM Customers;"
            cursor.execute(query)
            next_id = cursor.fetchone()[0]
            print(cursor)
            return next_id

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
                
    def get_all_products(self):
        try:
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            query = """
            SELECT Product_ID, Category, Price, Subcategory FROM Products
            """
            cursor.execute(query)
            result = cursor.fetchall()

            products = []
            for row in result:
                product = {
                    "item_id": row[0],
                    "name": row[1],          # Category as name
                    "sales_price": row[2],
                    "item_type": row[3]      # Subcategory as item_type
                }
                products.append(product)

            return products

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def get_all_services(self):
        try:
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            query = """
            SELECT Service_ID, Price, Max_Execution_Hours FROM Services
            """
            cursor.execute(query)
            result = cursor.fetchall()

            services = []
            for row in result:
                service = {
                    "item_id": row[0],
                    "name": f"Service with Max {row[2]} hours",  # Generate a name based on Max_Execution_Hours
                    "sales_price": row[1],
                    "item_type": "Service"
                }
                services.append(service)

            return services

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()


    def get_item_price(self, item_name):
        """
        Fetch the price of an item by its name from the database.
        :param item_name: The name of the item.
        :return: The price of the item, or None if not found.
        """
        try:
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            # Query to fetch price from Products and Services
            query = """
            SELECT sales_price FROM Products WHERE name = :item_name
            UNION ALL
            SELECT sales_price FROM Services WHERE name = :item_name
            """
            cursor.execute(query, {"item_name": item_name})
            result = cursor.fetchone()

            return result[0] if result else None

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def get_available_logins(self, table_name):
        """
        Retrieve available usernames and passwords from a specific table.
        :param table_name: The name of the table ('Customers' or 'Employees').
        :return: A list of dictionaries with 'username' and 'password'.
        """
        try:
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            query = f"SELECT Name, Password_Hash FROM {table_name}"
            cursor.execute(query)

            results = cursor.fetchall()
            logins = [{"username": row[0], "password": row[1]} for row in results]

            return logins

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
                
    def add_product(self, warehouse_id, zone_id, quantity, minimum_stock, price, category, subcategory, discount=None):
        try:
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            query = """
            INSERT INTO Products (Product_Warehouse_ID, Product_Zone_ID, Quantity_in_Stock, Minimum_Stock, Price, Category, Subcategory, Discount)
            VALUES (:warehouse_id, :zone_id, :quantity, :minimum_stock, :price, :category, :subcategory, :discount)
            """

            cursor.execute(query, {
                "warehouse_id": warehouse_id,
                "zone_id": zone_id,
                "quantity": quantity,
                "minimum_stock": minimum_stock,
                "price": price,
                "category": category,
                "subcategory": subcategory,
                "discount": discount
            })

            connection.commit()
            print("Product added successfully.")

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()



def create_order(self, user_details, total):
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        # Insert a new order into the Orders table
        query = """
        INSERT INTO Orders (Customer_ID, Delivery_Address, Status, Checkout_Total, Payment_Status, Shipping_Status)
        VALUES (:customer_id, :delivery_address, 'accepted', :checkout_total, 'paypal', 'in transit')
        """
        cursor.execute(query, {
            'customer_id': user_details['account_id'],
            'delivery_address': user_details['address'],
            'checkout_total': total
        })

        # Commit the transaction
        connection.commit()
        print("Order successfully created.")

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
    
def get_all_suppliers_for_item(self, item_name):
    """
    Fetch all supplier details for a given item name.
    :param item_name: The name of the item.
    :return: A list of supplier information or an empty list if not found.
    """
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        # SQL Query to get all supplier details for the given item name (without aliases)
        query = """
        SELECT Suppliers.Supplier_ID, 
               Suppliers.Name AS Supplier_Name, 
               Suppliers.Contact_Info, 
               SupplierItems.Price AS Supplier_Price, 
               SupplierItems.Availability
        FROM Suppliers
        JOIN SupplierItems ON Suppliers.Supplier_ID = SupplierItems.Supplier_ID
        JOIN Items ON Items.Item_ID = SupplierItems.Item_ID
        WHERE Items.Name = :item_name
        """

        cursor.execute(query, {"item_name": item_name})
        result = cursor.fetchall()

        # If no suppliers are found, return an empty list
        if not result:
            print(f"No suppliers found for item: {item_name}")
            return []

        # List of all supplier details
        suppliers = []
        for row in result:
            suppliers.append({
                "Supplier_ID": row[0],
                "Supplier_Name": row[1],
                "Contact_Info": row[2],
                "Supplier_Price": row[3],
                "Availability": row[4]
            })

        return suppliers

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def get_products_below_min_stock_with_suppliers(self):
    """
    Fetch products that have reached their minimum stock level along with their suppliers.
    :return: A list of products and their supplier information.
    """
    try:
        # Connect to the Oracle database
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        # SQL query to fetch products below minimum stock with supplier details
        query = """
        SELECT 
            Products.Product_ID,
            Products.Quantity_in_Stock,
            Products.Minimum_Stock,
            Products.Price,
            Products.Category,
            Products.Subcategory,
            Suppliers.Supplier_ID,
            Suppliers.Name AS Supplier_Name,
            Suppliers.Contact_Info
        FROM Products
        JOIN Items ON Products.Product_ID = Items.Item_ID
        JOIN SupplierItems ON Items.Item_ID = SupplierItems.Item_ID
        JOIN Suppliers ON SupplierItems.Supplier_ID = Suppliers.Supplier_ID
        WHERE Products.Quantity_in_Stock <= Products.Minimum_Stock
        """

        cursor.execute(query)
        result = cursor.fetchall()

        # If no results found, return an empty list
        if not result:
            print("No products have reached their minimum stock level.")
            return []

        # Format the results into a list of dictionaries
        products = []
        for row in result:
            products.append({
                "Product_ID": row[0],
                "Quantity_in_Stock": row[1],
                "Minimum_Stock": row[2],
                "Price": row[3],
                "Category": row[4],
                "Subcategory": row[5],
                "Supplier_ID": row[6],
                "Supplier_Name": row[7],
                "Contact_Info": row[8]
            })

        return products

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        return []
    finally:
        # Ensure resources are properly closed
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()



def get_product_by_name(self, product_name):
    """
    Fetch a specific product by its name (Category).
    :param product_name: The name (Category) of the product.
    :return: A dictionary representing the product or None if not found.
    """
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        query = """
        SELECT Product_ID, Category, Price, Subcategory
        FROM Products
        WHERE Category = :product_name
        """
        cursor.execute(query, {"product_name": product_name})
        row = cursor.fetchone()

        if row:
            product = {
                "item_id": row[0],
                "name": row[1],          # Category as name
                "sales_price": row[2],
                "item_type": row[3]      # Subcategory as item_type
            }
            return product
        else:
            return None

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def get_service_by_name(self, service_name):
    """
    Fetch a specific service by its generated name.
    :param service_name: The generated name of the service (based on Max_Execution_Hours).
    :return: A dictionary representing the service or None if not found.
    """
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        query = """
        SELECT Service_ID, Price, Max_Execution_Hours
        FROM Services
        WHERE Max_Execution_Hours = :max_hours
        """
        
        # Extract hours from the service name
        try:
            max_hours = int(service_name.split("Max ")[1].split(" hours")[0])
        except (IndexError, ValueError):
            print("Invalid service name format.")
            return None

        cursor.execute(query, {"max_hours": max_hours})
        row = cursor.fetchone()

        if row:
            service = {
                "item_id": row[0],
                "name": f"Service with Max {row[2]} hours",
                "sales_price": row[1],
                "item_type": "Service"
            }
            return service
        else:
            return None

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def get_aisles_for_high_discount_products(self):
    """
    Fetch the aisles where products with discounts greater than 20% 
    and the highest number of purchase orders are stored.
    :return: A list of dictionaries containing Zone_ID, Product_Name, Order_Count, Capacity.
    """
    try:
        # Establish connection to the database
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        # SQL Query to get the zones for products with discount > 20% and highest order counts
        query = """
        SELECT 
            Z.Zone_ID,
            Z.Capacity,
            P.Product_ID,
            P.Name AS Product_Name,
            COUNT(OI.Order_Item_ID) AS Order_Count
        FROM 
            Products P
        JOIN 
            OrderItem OI ON P.Product_ID = OI.FK_Item_ID
        JOIN 
            Orders O ON OI.FK_Order_ID = O.Order_ID
        JOIN 
            Zones Z ON P.Product_Zone_ID = Z.Zone_ID
        WHERE 
            P.Discount > 20
            AND O.Status = 'accepted'  -- Ensure we're counting only accepted orders
        GROUP BY 
            Z.Zone_ID, Z.Capacity, P.Product_ID, P.Name
        ORDER BY 
            Order_Count DESC;  -- Get the zones where products with the highest orders are stored
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Prepare the result list
        aisles_info = []
        for row in results:
            aisle_data = {
                "Zone_ID": row[0],
                "Capacity": row[1],
                "Product_Name": row[3],
                "Order_Count": row[4]
            }
            aisles_info.append(aisle_data)

        return aisles_info

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        # Clean up: close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def get_orders_by_day_and_time(self, specific_date):
    """
    Fetch orders that are scheduled for delivery on a specific date.
    :param specific_date: The date for which we need to fetch orders (format: 'YYYY-MM-DD')
    :return: A list of dictionaries containing Order ID, Customer ID, Delivery Address, Shipping Status, and Checkout Total.
    """
    try:
        # Establish connection to the database
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
        cursor = connection.cursor()

        # SQL Query to get orders scheduled for delivery on a specific date
        query = """
        SELECT 
            O.Order_ID,
            O.Customer_ID,
            O.Delivery_Address,
            O.Status,
            O.Shipping_Status,
            O.Checkout_Total
        FROM 
            Orders O
        WHERE 
            TO_DATE(O.Shipping_Status) = TO_DATE(:specific_date, 'YYYY-MM-DD') 
            AND TO_TIMESTAMP(O.Shipping_Status) BETWEEN TO_TIMESTAMP(:specific_date || ' 00:00:00', 'YYYY-MM-DD HH24:MI:SS') 
            AND TO_TIMESTAMP(:specific_date || ' 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
        """

        # Execute the query with the specified date
        cursor.execute(query, {'specific_date': specific_date})

        # Fetch all the results
        results = cursor.fetchall()

        # Prepare the result list
        orders_info = []
        for row in results:
            order_data = {
                "Order_ID": row[0],
                "Customer_ID": row[1],
                "Delivery_Address": row[2],
                "Status": row[3],
                "Shipping_Status": row[4],
                "Checkout_Total": row[5]
            }
            orders_info.append(order_data)

        return orders_info

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        # Clean up: close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()



class Mongodb():
    def create_rating(self, customer_name, item_name, rating, comment=None, attachments=None):
        try:
            # Connect to Oracle Database to get customer_id and item_id
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()
            
            # Fetch customer_id based on customer_name
            cursor.execute("SELECT Account_ID FROM Customers WHERE Name = :name", {"name": customer_name})
            customer_result = cursor.fetchone()
            if not customer_result:
                print("Customer not found.")
                return
            
            customer_id = customer_result[0]
            
            # Fetch item_id based on item_name
            cursor.execute("SELECT Item_ID FROM Items WHERE Name = :name", {"name": item_name})
            item_result = cursor.fetchone()
            if not item_result:
                print("Item not found.")
                return
            
            item_id = item_result[0]
            
            # Prepare the rating document
            rating_doc = {
                "customer_id": customer_id,
                "item_id": item_id,
                "rating": rating,  # Initial rating set to 0
                "comment": comment if comment else "",
                "attachments": attachments if attachments else []
            }
            
            # Insert the document into MongoDB
            result = ratings_collection.insert_one(rating_doc)
            print(f"Rating created successfully with ID: {result.inserted_id}")

        except cx_Oracle.DatabaseError as e:
            print(f"Oracle Database error: {e}")
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
    def record_browsing_history(self, customer_id, page_url):
        """
        Records browsing history for a customer.
        
        :param customer_id: The ID of the customer.
        :param page_url: The URL of the visited page.
        """
        try:
            # Get the current date and time in UTC using timezone-aware datetime
            visit_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            visit_time = datetime.now(timezone.utc).strftime("%H:%M:%S")

            # Create the browsing history document
            history_doc = {
                "customer_id": customer_id,
                "page": page_url,
                "visit_date": visit_date,
                "visit_time": visit_time
            }
            
            # Insert the document into MongoDB
            result = browsing_collection.insert_one(history_doc)
            print(f"Browsing history recorded successfully with ID: {result.inserted_id}")
        
        except Exception as e:
            print(f"Error recording browsing history: {e}")
    
    def get_browsing_history(self, customer_id):
        """
        Retrieves browsing history for a specific customer.
        
        :param customer_id: The ID of the customer.
        """
        try:
            # Query the browsing history for the customer
            records = browsing_collection.find({"customer_id": customer_id})
            
            print(f"\n--- Browsing History for Customer ID: {customer_id} ---")
            for record in records:
                print(f"Page: {record['page']}, Date: {record['visit_date']}, Time: {record['visit_time']}")
        
        except Exception as e:
            print(f"Error retrieving browsing history: {e}")