-- 2. DUPLICATES: primary keys

SELECT 'customers.customer_id' AS check_name, customer_id AS dup_key, COUNT(*) AS n
FROM customers GROUP BY customer_id HAVING n > 1
UNION ALL
SELECT 'products.product_id', product_id, COUNT(*)
FROM products GROUP BY product_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'categories.category_id', category_id, COUNT(*)
FROM categories GROUP BY category_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'orders.order_id', order_id, COUNT(*)
FROM orders GROUP BY order_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'order_items.order_item_id', order_item_id, COUNT(*)
FROM order_items GROUP BY order_item_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'suppliers.supplier_id', supplier_id, COUNT(*)
FROM suppliers GROUP BY supplier_id HAVING COUNT(*) > 1;
