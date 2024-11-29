-- Create the data base
CREATE DATABASE Project_TABDD;
GO

USE Project_TABDD;
GO

-- Table Customers
CREATE TABLE Customers (
    Customer_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Name VARCHAR(25) NULL,
    Address VARCHAR(50) NOT NULL,
    Postal_Code VARCHAR(15) NOT NULL,
    NIF VARCHAR(15) NOT NULL,
    Email VARCHAR(35) NOT NULL UNIQUE,
    Account_ID INT NOT NULL UNIQUE,
    Password_Hash VARCHAR(20) NOT NULL,
    GDPR_Terms TEXT NOT NULL,
    Accepted_Date DATE NOT NULL,
    Points_Balance INT NULL DEFAULT 0,
    Last_Points_Redeemed_date DATE NULL,
    Status VARCHAR(10) NOT NULL CHECK (Status IN ('new', 'active', 'blocked', 'prohibited'))
);
GO

-- Table Employees
CREATE TABLE Employees (
    Employee_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Name VARCHAR(25) NOT NULL,
    Account_ID VARCHAR(20) NOT NULL UNIQUE,
    Email VARCHAR(35) NOT NULL UNIQUE,
    Password_Hash VARCHAR(20) NOT NULL,
    Role VARCHAR(15) NOT NULL
);
GO

-- Table Items
CREATE TABLE Items (
    Item_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Name VARCHAR(20) NULL,
    Description VARCHAR(50) NOT NULL,
    Brand VARCHAR(20) NOT NULL,
    Type VARCHAR(20) NOT NULL CHECK (Type IN ('Service', 'Product')),
    Primary_Supplier_ID INT NOT NULL,
    Purchase_price FLOAT NOT NULL,
    Sales_Price FLOAT NOT NULL
);
GO

-- Table OrderItem
CREATE TABLE OrderItem (
    Order_Item_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    FK_Item_ID INT NOT NULL,
    FK_Order_ID INT NOT NULL,
    Quantity INT NOT NULL,
    Price FLOAT NOT NULL
);
GO

-- Table Orders
CREATE TABLE Orders (
    Order_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Delivery_Address VARCHAR(25) NOT NULL,
    Status VARCHAR(15) NOT NULL CHECK (Status IN ('accepted', 'suspended')),
    Checkout_Total FLOAT NOT NULL,
    Payment_Status VARCHAR(15) NOT NULL,
    Shipping_status VARCHAR(15) NOT NULL CHECK (Shipping_status IN ('in transit', 'delivered'))
);
GO

-- Table Products
CREATE TABLE Products (
    Product_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Product_Warehouse_ID INT NOT NULL,
    Product_Zone_ID INT NOT NULL,
    Quantity_in_Stock INT NOT NULL,
    Minimum_Stock INT NOT NULL,
    Price FLOAT NOT NULL,
    Category VARCHAR(15) NOT NULL,
    Subcategory VARCHAR(15) NOT NULL,
	Discount FLOAT NULL
);
GO

-- Table ProductPrices
CREATE TABLE ProductPrices (
	Product_ID INT NOT NULL,
	Price FLOAT NOT NULL,
	Initial_date DATE NOT NULL,
	Final_date DATE NOT NULL,
	CONSTRAINT PK_ProductPrices PRIMARY KEY (Product_ID, Price)
);
GO

-- Table Services
CREATE TABLE Services (
    Service_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Max_Execution_Hours INT NOT NULL,
    Execution_Time FLOAT NOT NULL,
    Responsible_Employee_ID INT NOT NULL,
    Price FLOAT NOT NULL,
);
GO

-- Table SupplierItems
CREATE TABLE SupplierItems (
    Supplier_Item_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Supplier_ID INT NOT NULL,
    Item_ID INT NOT NULL,
    Price FLOAT NOT NULL,
    Availability VARCHAR(10) NOT NULL
);
GO

-- Table Suppliers
CREATE TABLE Suppliers (
    Supplier_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Name VARCHAR(20) NULL,
    Contact_Info VARCHAR(20) NOT NULL,
    Best_Selling_Item_ID INT NOT NULL
);
GO

-- Table Vouchers
CREATE TABLE Vouchers (
    Voucher_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Customer_ID INT NOT NULL,
    Amount FLOAT NOT NULL,
    Valid_until DATE NOT NULL
);
GO

-- Table Warehouses
CREATE TABLE Warehouses (
    Warehouse_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Name NVARCHAR(15) NOT NULL UNIQUE,
    Address NVARCHAR(50) NOT NULL,
    Location NCHAR(10) NOT NULL
);
GO

-- Table Zones
CREATE TABLE Zones (
    Zone_ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Capacity INT NOT NULL,
    Warehouse_ID INT NOT NULL
);
GO

-- Relations (FOREIGN KEY)
-- Items
ALTER TABLE Items ADD CONSTRAINT Primary_Supplier_ID_FK FOREIGN KEY (Primary_Supplier_ID)
REFERENCES Suppliers (Supplier_ID);
GO

-- OrderItem
ALTER TABLE OrderItem ADD CONSTRAINT FK_Item_ID FOREIGN KEY (FK_Item_ID)
REFERENCES Items (Item_ID);
GO
ALTER TABLE OrderItem ADD CONSTRAINT FK_Order_ID FOREIGN KEY (FK_Order_ID)
REFERENCES Orders (Order_ID);
GO

-- Orders
ALTER TABLE Orders ADD CONSTRAINT Customer_ID_FK FOREIGN KEY (Customer_ID)
REFERENCES Customers (Customer_ID);
GO

-- Products
ALTER TABLE Products ADD CONSTRAINT Product_Warehouse_ID_FK FOREIGN KEY (Product_Warehouse_ID)
REFERENCES Warehouses (Warehouse_ID);
GO
ALTER TABLE Products ADD CONSTRAINT Product_Zone_ID_FK FOREIGN KEY (Product_Zone_ID)
REFERENCES Zones (Zone_ID);
GO
ALTER TABLE Products ADD CONSTRAINT Product_ID_FK FOREIGN KEY (Product_ID)
REFERENCES Items (Item_ID);
GO

-- ProductPrices
ALTER TABLE ProductPrices ADD CONSTRAINT PP_Product_ID_FK FOREIGN KEY (Product_ID)
REFERENCES Products (Product_ID);
GO

-- Services
ALTER TABLE Services ADD CONSTRAINT Responsible_Employee_ID_FK FOREIGN KEY (Responsible_Employee_ID)
REFERENCES Employees (Employee_ID);
GO
ALTER TABLE Services ADD CONSTRAINT Service_ID_FK FOREIGN KEY (Service_ID)
REFERENCES Items (Item_ID);
GO

-- SupplierItems
ALTER TABLE SupplierItems ADD CONSTRAINT Supplier_ID_FK FOREIGN KEY (Supplier_ID)
REFERENCES Suppliers (Supplier_ID);
GO
ALTER TABLE SupplierItems ADD CONSTRAINT Item_ID_FK FOREIGN KEY (Item_ID)
REFERENCES Items (Item_ID);
GO

-- Suppliers
ALTER TABLE Suppliers ADD CONSTRAINT Best_Selling_Item_ID_FK FOREIGN KEY (Best_Selling_Item_ID)
REFERENCES Items (Item_ID);
GO

-- Vouchers
ALTER TABLE Vouchers ADD CONSTRAINT FK_Customer_ID FOREIGN KEY (Customer_ID)
REFERENCES Customers (Customer_ID);
GO

-- Zones
ALTER TABLE Zones ADD CONSTRAINT Warehouse_ID_FK FOREIGN KEY (Warehouse_ID)
REFERENCES Warehouses (Warehouse_ID);
GO
