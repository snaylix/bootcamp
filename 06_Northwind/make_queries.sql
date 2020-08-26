-- 1. Get the names and the quantities in stock for each product.
SELECT product_name, quantity_per_unit, units_in_stock FROM products;

-- 2. Get a list of current products (Product ID and name).
SELECT product_ID, product_name FROM products;

-- 3. Get a list of the most and least expensive products (name and unit price).
SELECT product_name, unit_price AS "Most expensive"
FROM products
ORDER BY unit_price DESC
LIMIT 10;

SELECT product_name, unit_price AS "Least expensive"
FROM products
ORDER BY unit_price ASC
LIMIT 10;

-- 4. Get products that cost less than $20.
SELECT product_name, unit_price AS "cheaper than 20 bucks"
FROM products
WHERE unit_price < 20;

-- 5. Get products that cost between $15 and $25.
SELECT product_name, unit_price AS "between $15-$25"
FROM products
WHERE unit_price >= 15 AND unit_price <= 25;

-- 6. Get products above average price.
SELECT product_name, unit_pric AS "above average"
FROM products
WHERE unit_price > average;
