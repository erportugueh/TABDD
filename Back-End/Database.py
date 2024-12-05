import cx_Oracle

from datetime import datetime


 # Database connection parameters
host = "vsgate-s1.dei.isep.ipp.pt"
port = "10434"
sid = "xe"
dsn_tns = cx_Oracle.makedsn(host, port, sid)
username = "C##admin_elmer"  # Replace with your database username
password = "AkNrX9qnAEQMO360inA4"  # Replace with your database password

class Database():

    # Function to save customer data into the database
    def save_customer_to_db(self, customer_data):
        try:
            # Connect to the database
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
            query = "SELECT AccountID_Sequence.NEXTVAL FROM DUAL"
            cursor.execute(query)
            next_id = cursor.fetchone()[0]

            return next_id

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def verify_login(self, username, password):
        """
        Verify login credentials against the database.
        :param username: The username provided by the user.
        :param password: The plaintext password provided by the user.
        :return: A dictionary with user details if credentials are correct, None otherwise.
        """
        try:
            # Connect to the database
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            # Query to check username and hashed password for both employees and customers
            query = """
            SELECT Account_ID, Name, 'employee' AS UserType
            FROM Employees
            WHERE Name = :username AND Password_Hash = :password_hash
            UNION ALL
            SELECT Account_ID, Name, 'customer' AS UserType
            FROM Customers
            WHERE Name = :username AND Password_Hash = :password_hash
            """
            
            # Hash the password (use the same hashing method as in registration)
            password_hash = str(hash(password))
            
            # Execute the query
            cursor.execute(query, username=username, password_hash=password_hash)
            result = cursor.fetchone()

            if result:
                # Extract details into a dictionary
                user_details = {
                    "account_id": result[0],
                    "name": result[1],
                    "type": result[2],  # Either 'employee' or 'customer'
                }
                return user_details

            return None  # Invalid credentials

        except cx_Oracle.DatabaseError as e:
            print(f"Database error: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()



    # Function to fetch all products from the database
    def get_all_products(self):
        try:
            # Connect to the database
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            # Query to fetch all products
            query = """
            SELECT item_id, name, sales_price, item_type FROM Products
            """
            cursor.execute(query)
            result = cursor.fetchall()

            products = []
            for row in result:
                product = {
                    "item_id": row[0],
                    "name": row[1],
                    "sales_price": row[2],
                    "item_type": row[3]
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

    # Function to fetch all services from the database
    def get_all_services(self):
        try:
            # Connect to the database
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
            cursor = connection.cursor()

            # Query to fetch all services
            query = """
            SELECT item_id, name, sales_price, item_type FROM Services
            """
            cursor.execute(query)
            result = cursor.fetchall()

            services = []
            for row in result:
                service = {
                    "item_id": row[0],
                    "name": row[1],
                    "sales_price": row[2],
                    "item_type": row[3]
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