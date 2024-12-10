-- Table Customers
CREATE TABLE Customers (
    Customer_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Name VARCHAR2(25),
    Address VARCHAR2(50) NOT NULL,
    Postal_Code VARCHAR2(15) NOT NULL,
    NIF VARCHAR2(15) NOT NULL,
    Email VARCHAR2(35) NOT NULL UNIQUE,
    Account_ID NUMBER NOT NULL UNIQUE,
    Password_Hash VARCHAR2(20) NOT NULL,
    GDPR_Terms CLOB NOT NULL,
    Accepted_Date DATE NOT NULL,
    Points_Balance NUMBER DEFAULT 0,
    Last_Points_Redeemed_date DATE,
    Status VARCHAR2(10) NOT NULL CHECK (Status IN ('new', 'active', 'blocked', 'prohibited'))
);

-- Table Employees
CREATE TABLE Employees (
    Employee_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Name VARCHAR2(25) NOT NULL,
    Account_ID VARCHAR2(20) NOT NULL UNIQUE,
    Email VARCHAR2(35) NOT NULL UNIQUE,
    Password_Hash VARCHAR2(20) NOT NULL,
    Role VARCHAR2(15) NOT NULL
);

-- Table Items
CREATE TABLE Items (
    Item_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Name VARCHAR2(20),
    Description VARCHAR2(50) NOT NULL,
    Brand VARCHAR2(20) NOT NULL,
    Type VARCHAR2(20) NOT NULL CHECK (Type IN ('Service', 'Product')),
    Primary_Supplier_ID NUMBER NOT NULL,
    Purchase_Price NUMBER NOT NULL,
    Sales_Price NUMBER NOT NULL
);

-- Table Services
CREATE TABLE Services (
    Service_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Item_ID NUMBER NOT NULL,
    Max_Execution_Hours NUMBER NOT NULL,
    Execution_Time NUMBER NOT NULL,
    Responsible_Employee_ID NUMBER NOT NULL,
    Price NUMBER NOT NULL
);

-- Table SupplierItems
CREATE TABLE SupplierItems (
    Supplier_Item_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Supplier_ID NUMBER NOT NULL,
    Item_ID NUMBER NOT NULL,
    Price NUMBER NOT NULL,
    Availability VARCHAR2(10) NOT NULL
);

-- Table Suppliers
CREATE TABLE Suppliers (
    Supplier_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Name VARCHAR2(20),
    Contact_Info VARCHAR2(20) NOT NULL,
    Best_Selling_Item_ID NUMBER NULL
);

-- Table Vouchers
CREATE TABLE Vouchers (
    Voucher_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Customer_ID NUMBER NOT NULL,
    Amount NUMBER NOT NULL,
    Valid_Until DATE NOT NULL
);

-- Table Warehouses
CREATE TABLE Warehouses (
    Warehouse_ID NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    Name VARCHAR2(15) NOT NULL UNIQUE,
    Address VARCHAR2(50) NOT NULL,
    Location CHAR(10) NOT NULL,
    Capacity NUMBER NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL
);

-- Table Zones
CREATE TABLE Zones (
    Zone_ID NUMBER GENERATED BY DEFAULT AS IDENTITY,
    Capacity NUMBER NOT NULL,
    Warehouse_ID NUMBER NOT NULL,
    CONSTRAINT Zone_PK PRIMARY KEY (Warehouse_ID, Zone_ID)
);

-- Table Aisles
CREATE TABLE Aisles (
    Aisle_ID NUMBER GENERATED BY DEFAULT AS IDENTITY,
    Capacity NUMBER NOT NULL,
    Zone_ID NUMBER NOT NULL,
    Warehouse_ID NUMBER NOT NULL,
    CONSTRAINT Aisle_PK PRIMARY KEY (Warehouse_ID, Zone_ID, Aisle_ID)
);

-- Add Foreign Key Constraints

-- Items
ALTER TABLE Items ADD CONSTRAINT Primary_Supplier_ID_FK FOREIGN KEY (Primary_Supplier_ID)
REFERENCES Suppliers (Supplier_ID);

-- ProductPrices
ALTER TABLE ProductPrices ADD CONSTRAINT PP_Product_ID_FK FOREIGN KEY (Product_ID)
REFERENCES Products (Product_ID);

-- Services
ALTER TABLE Services ADD CONSTRAINT Responsible_Employee_ID_FK FOREIGN KEY (Responsible_Employee_ID)
REFERENCES Employees (Employee_ID);
ALTER TABLE Services ADD CONSTRAINT Service_Item_ID_FK FOREIGN KEY (Item_ID)
REFERENCES Items (Item_ID);

-- SupplierItems
ALTER TABLE SupplierItems ADD CONSTRAINT Supplier_ID_FK FOREIGN KEY (Supplier_ID)
REFERENCES Suppliers (Supplier_ID);
ALTER TABLE SupplierItems ADD CONSTRAINT Item_ID_FK FOREIGN KEY (Item_ID)
REFERENCES Items (Item_ID);

-- Vouchers
ALTER TABLE Vouchers ADD CONSTRAINT FK_Customer_ID FOREIGN KEY (Customer_ID)
REFERENCES Customers (Customer_ID);

-- Zones
ALTER TABLE Zones ADD CONSTRAINT Warehouse_ID_FK FOREIGN KEY (Warehouse_ID)
REFERENCES Warehouses (Warehouse_ID);


--Aisles
ALTER TABLE Aisles ADD CONSTRAINT Aisle_Warehouse_ID_FK FOREIGN KEY (Warehouse_ID)
REFERENCES Warehouses (Warehouse_ID);
ALTER TABLE Aisles ADD CONSTRAINT Aisle_Zone_ID_FK FOREIGN KEY (Zone_ID)
REFERENCES Zones (Zone_ID);