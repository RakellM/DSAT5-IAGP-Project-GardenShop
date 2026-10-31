-- 3. DUPLICATES: natural / business keys

SELECT 'customer email' AS check_name, email AS dup_value, COUNT(*) AS n
FROM customers GROUP BY email HAVING n > 1
UNION ALL
SELECT 'product name', product_name, COUNT(*)
FROM products GROUP BY product_name HAVING COUNT(*) > 1
UNION ALL
SELECT 'category name', category_name, COUNT(*)
FROM categories GROUP BY category_name HAVING COUNT(*) > 1
UNION ALL
SELECT 'supplier name', supplier_name, COUNT(*)
FROM suppliers GROUP BY supplier_name HAVING COUNT(*) > 1
UNION ALL
SELECT 'order_id+product_id', order_id || '|' || product_id, COUNT(*)
FROM order_items GROUP BY order_id, product_id HAVING COUNT(*) > 1;
