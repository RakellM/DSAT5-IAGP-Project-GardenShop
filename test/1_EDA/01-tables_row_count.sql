
-- 1. ROW COUNTS

SELECT 'customers'   AS table_name, COUNT(*) AS rows, 20 AS expected FROM customers
UNION ALL SELECT 'products',   COUNT(*), 24 FROM products
UNION ALL SELECT 'categories', COUNT(*),  8 FROM categories
UNION ALL SELECT 'orders',     COUNT(*), 24 FROM orders
UNION ALL SELECT 'order_items',COUNT(*), 48 FROM order_items
UNION ALL SELECT 'suppliers',  COUNT(*),  6 FROM suppliers;


SELECT COUNT(*) AS total_rows,
       (SELECT COUNT(*) FROM customers)
     + (SELECT COUNT(*) FROM products)
     + (SELECT COUNT(*) FROM categories)
     + (SELECT COUNT(*) FROM orders)
     + (SELECT COUNT(*) FROM order_items)
     + (SELECT COUNT(*) FROM suppliers) AS recomputed_total
FROM customers LIMIT 1;


