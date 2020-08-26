DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS categories (
  category_ID SERIAL PRIMARY KEY,
  category_Name VARCHAR(50),
  description TEXT
);

CREATE TABLE IF NOT EXISTS customers (
  customer_ID CHAR(5) PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(100) NOT NULL,
  contact_title VARCHAR(100) NOT NULL,
  address VARCHAR(100) NOT NULL,
  city VARCHAR(50) NOT NULL,
  region VARCHAR(50),
  postal_Code VARCHAR(15),
  country VARCHAR(100),
  phone VARCHAR(25),
  fax VARCHAR(25)
);

CREATE TABLE IF NOT EXISTS employees (
  employee_ID SERIAL PRIMARY KEY,
  last_name VARCHAR(50) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  job_title VARCHAR(100) NOT NULL,
  courtesy_title VARCHAR(10) NOT NULL,
  birth_date TIMESTAMP NOT NULL,
  hire_date TIMESTAMP NOT NULL,
  address VARCHAR(100) NOT NULL,
  city VARCHAR(50) NOT NULL,
  region VARCHAR(5),
  postal_Code VARCHAR(15) NOT NULL,
  country VARCHAR(50) NOT NULL,
  phone VARCHAR(25),
  extension SMALLINT,
  notes TEXT,
  reports_to SMALLINT,
  photo_path VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS employee_territories (
  emplyee_ID SMALLINT NOT NULL,
  territory_ID BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_details (
  order_ID INTEGER NOT NULL,
  product_ID SMALLINT NOT NULL,
  unit_price REAL NOT NULL,
  quantity SMALLINT NOT NULL,
  discount REAL
);

CREATE TABLE IF NOT EXISTS orders (
  order_ID SERIAL PRIMARY KEY,
  customer_ID CHAR(5) NOT NULL,
  employee_ID SMALLINT NOT NULL,
  order_date TIMESTAMP NOT NULL,
  required_date TIMESTAMP NOT NULL,
  shipped_date VARCHAR(50),
  shipped_via SMALLINT NOT NULL,
  freight REAL NOT NULL,
  ship_name VARCHAR (50) NOT NULL,
  ship_address VARCHAR (100) NOT NULL,
  ship_city VARCHAR(50) NOT NULL,
  ship_region VARCHAR(25),
  ship_postal_code VARCHAR(25),
  ship_country VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS products (
  product_ID SERIAL PRIMARY KEY,
  product_name VARCHAR(100) NOT NULL,
  supplier_ID SMALLINT NOT NULL,
  category_ID SMALLINT NOT NULL,
  quantity_per_unit VARCHAR(50) NOT NULL,
  unit_price REAL NOT NULL,
  units_in_stock SMALLINT NOT NULL,
  units_on_order SMALLINT NOT NULL,
  reorder_level SMALLINT NOT NULL,
  discontinued BOOLEAN
);

CREATE TABLE IF NOT EXISTS regions (
  region_ID SERIAL PRIMARY KEY CHECK (region_ID<5),
  region_description VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS shippers (
  shipper_id SERIAL PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  phone VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS suppliers (
  supplier_ID SERIAL PRIMARY KEY,
  company_name VARCHAR(100) NOT NULL,
  contact_name VARCHAR(100),
  contact_title VARCHAR(100),
  address VARCHAR(100) NOT NULL,
  city VARCHAR(50) NOT NULL,
  region VARCHAR(25) NOT NULL,
  postal_code VARCHAR(15) NOT NULL,
  country VARCHAR(100) NOT NULL,
  phone VARCHAR(25),
  fax VARCHAR(25),
  homepage TEXT
);

CREATE TABLE IF NOT EXISTS territories (
  territory_ID INTEGER PRIMARY KEY,
  territory_description VARCHAR(50) NOT NULL,
  region_ID SMALLINT CHECK (region_ID<5)
);

COPY categories FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/categories.csv' DELIMITER ',' CSV HEADER;
COPY customers FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/customers.csv' DELIMITER ',' CSV HEADER;
COPY employees FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/employees.csv' DELIMITER ',' CSV HEADER;
COPY employee_territories FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/employee_territories.csv' DELIMITER ',' CSV HEADER;
COPY order_details FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/order_details.csv' DELIMITER ',' CSV HEADER;
COPY orders FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/orders.csv' DELIMITER ',' CSV HEADER;
COPY products FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/products.csv' DELIMITER ',' CSV HEADER;
COPY regions FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/regions.csv' DELIMITER ',' CSV HEADER;
COPY shippers FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/shippers.csv' DELIMITER ',' CSV HEADER;
COPY suppliers FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/suppliers.csv' DELIMITER ',' CSV HEADER;
COPY territories FROM '/home/snay/01_repositories/logistic-lemongrass-student-code/06_week/_RES/data/territories.csv' DELIMITER ',' CSV HEADER;
