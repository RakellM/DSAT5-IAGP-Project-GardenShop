-- 4. MISSING VALUES: per table, every column

-- 4a. customers
SELECT 'customers' AS table_name,
       SUM(phone        IS NULL) AS phone_nulls,
       SUM(email        IS NULL) AS email_nulls,
       SUM(signup_date  IS NULL) AS signup_nulls,
       SUM(is_active    IS NULL) AS is_active_nulls
FROM customers;

-- 4b. orders
SELECT 'orders' AS table_name,
       SUM(shipped_date IS NULL) AS shipped_date_nulls,
       SUM(coupon_code  IS NULL) AS coupon_nulls,
       SUM(status       IS NULL) AS status_nulls,
       SUM(customer_id  IS NULL) AS customer_nulls
FROM orders;

-- 4c. products
SELECT 'products' AS table_name,
       SUM(price             IS NULL) AS price_nulls,
       SUM(cost              IS NULL) AS cost_nulls,
       SUM(quantity_on_hand  IS NULL) AS qty_nulls,
       SUM(reorder_level     IS NULL) AS reorder_nulls,
       SUM(discontinued      IS NULL) AS discontinued_nulls
FROM products;

-- 4d. suppliers
SELECT 'suppliers' AS table_name,
       SUM(contact_email IS NULL) AS email_nulls,
       SUM(state         IS NULL) AS state_nulls
FROM suppliers;

-- 4e. order_items
SELECT 'order_items' AS table_name,
       SUM(order_id   IS NULL) AS order_nulls,
       SUM(product_id IS NULL) AS product_nulls,
       SUM(quantity   IS NULL) AS qty_nulls,
       SUM(unit_price IS NULL) AS price_nulls
FROM order_items;
