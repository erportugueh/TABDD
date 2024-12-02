-- Create a user named 'test_user' with password 'password123'
CREATE USER C##admin_elmer IDENTIFIED BY AkNrX9qnAEQMO360inA4;
-- Grant CONNECT access to allow the user to log in
GRANT CONNECT TO  C##admin_elmer;
GRANT RESOURCE TO  C##admin_elmer;
ALTER USER  C##admin_elmer QUOTA UNLIMITED ON users;

-- Create a user named 'test_user' with password 'password123'
CREATE USER C##admin_vasco IDENTIFIED BY SjWnMwDxFAaFRsPdG8zb;
-- Grant CONNECT access to allow the user to log in
GRANT CONNECT TO  C##admin_vasco;
GRANT RESOURCE TO  C##admin_vasco;
ALTER USER  C##admin_vasco QUOTA UNLIMITED ON users;

-- Create a user named 'test_user' with password 'password123'
CREATE USER C##admin_rebeca IDENTIFIED BY b6HJ1lbarsCxfbVUY4Wn;
-- Grant CONNECT access to allow the user to log in
GRANT CONNECT TO  C##admin_rebeca;
GRANT RESOURCE TO  C##admin_rebeca;
ALTER USER  C##admin_rebeca QUOTA UNLIMITED ON users;

-- Create a user named 'test_user' with password 'password123'
CREATE USER C##admin_franscisca IDENTIFIED BY fPOt1DMjpUMrafiRlH40;
-- Grant CONNECT access to allow the user to log in
GRANT CONNECT TO  C##admin_franscisca;
GRANT RESOURCE TO  C##admin_franscisca;
ALTER USER  C##admin_franscisca QUOTA UNLIMITED ON users;

GRANT DBA TO C##admin_elmer;
GRANT DBA TO C##admin_vasco;
GRANT DBA TO C##admin_rebeca;
GRANT DBA TO C##admin_franscisca;

-- Create the database
-- Oracle does not use `CREATE DATABASE` for individual databases like SQL Server.
-- Instead, schemas are used within a single database.
-- Create a user/schema (optional step for Oracle):
CREATE USER project_tabdd IDENTIFIED BY your_password;
GRANT CONNECT, RESOURCE TO project_tabdd;
ALTER USER project_tabdd QUOTA UNLIMITED ON USERS;
