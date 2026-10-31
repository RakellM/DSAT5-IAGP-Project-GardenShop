-- 5. REFERENTIAL INTEGRITY

SELECT 'order_items -> orders' AS fk, oi.order_id AS orphan_value
FROM order_items oi
LEFT JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'order_items -> products', oi.product_id
FROM order_items oi
LEFT JOIN products p ON p.product_id = oi.product_id
WHERE p.product_id IS NULL
UNION ALL
SELECT 'orders -> customers', o.customer_id
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
UNION ALL
SELECT 'products -> categories', p.category_id
FROM products p
LEFT JOIN categories c ON c.category_id = p.category_id
WHERE c.category_id IS NULL
UNION ALL
SELECT 'products -> suppliers', p.supplier_id
FROM products p
LEFT JOIN suppliers s ON s.supplier_id = p.supplier_id
WHERE s.supplier_id IS NULL;
